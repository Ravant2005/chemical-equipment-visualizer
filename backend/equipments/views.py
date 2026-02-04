from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Dataset, Equipment
from .serializers import DatasetSerializer, EquipmentSerializer
import pandas as pd


class DatasetViewSet(ModelViewSet):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')
    
    def perform_create(self, serializer):
        """Set the user when creating a dataset"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload a CSV file with equipment data"""
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return Response({'error': 'Only CSV files allowed'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_csv(file)
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            
            if not all(col in df.columns for col in required_columns):
                return Response(
                    {'error': f'Missing required columns. Expected: {", ".join(required_columns)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            total_count = len(df)
            avg_flowrate = float(df['Flowrate'].mean())
            avg_pressure = float(df['Pressure'].mean())
            avg_temperature = float(df['Temperature'].mean())
            equipment_distribution = df['Type'].value_counts().to_dict()
            
            dataset = Dataset.objects.create(
                user=request.user,
                filename=file.name,
                total_count=total_count,
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature,
                equipment_distribution=equipment_distribution
            )
            
            equipment_records = []
            for _, row in df.iterrows():
                equipment_records.append(Equipment(
                    dataset=dataset,
                    equipment_name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature'])
                ))
            
            Equipment.objects.bulk_create(equipment_records)
            
            # Keep only last 5 datasets
            user_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
            if user_datasets.count() > 5:
                for ds in user_datasets[5:]:
                    ds.delete()
            
            return Response(DatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get upload history for the current user (last 5)"""
        datasets = self.get_queryset()[:5]
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)


class EquipmentViewSet(ReadOnlyModelViewSet):
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Equipment.objects.filter(dataset__user=self.request.user).order_by('-id')

