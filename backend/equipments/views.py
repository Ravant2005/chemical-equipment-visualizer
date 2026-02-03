from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset, Equipment
from .serializers import DatasetSerializer
import pandas as pd
import csv
import io

class DatasetViewSet(ModelViewSet):
    serializer_class = DatasetSerializer
    
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)[:5]
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return Response({'error': 'Only CSV files allowed'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_csv(file)
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            
            if not all(col in df.columns for col in required_columns):
                return Response({'error': 'Missing required columns'}, status=status.HTTP_400_BAD_REQUEST)
            
            total_count = len(df)
            avg_flowrate = df['Flowrate'].mean()
            avg_pressure = df['Pressure'].mean()
            avg_temperature = df['Temperature'].mean()
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
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature']
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
        datasets = self.get_queryset()
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)