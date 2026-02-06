from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.utils.timezone import localtime
from .models import Dataset, Equipment
from .serializers import DatasetSerializer, EquipmentSerializer
import pandas as pd


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_simple_pdf(lines):
    content_lines = ["BT", "/F1 12 Tf", "72 720 Td"]
    for idx, line in enumerate(lines):
        if idx > 0:
            content_lines.append("0 -16 Td")
        content_lines.append(f"({_escape_pdf_text(line)}) Tj")
    content_lines.append("ET")
    content = "\n".join(content_lines).encode("latin-1", "replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n%\xE2\xE3\xCF\xD3\n")

    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode("latin-1"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode("latin-1")
    )
    return bytes(pdf)


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

    @action(detail=True, methods=['get'])
    def generate_report(self, request, pk=None):
        """Generate a simple PDF report for the dataset"""
        dataset = self.get_object()
        uploaded_at = localtime(dataset.uploaded_at).strftime('%Y-%m-%d %H:%M:%S %Z')
        distribution = dataset.equipment_distribution or {}
        distribution_lines = [
            f"{key}: {value}" for key, value in sorted(distribution.items(), key=lambda item: item[1], reverse=True)
        ][:10]

        lines = [
            "Chemical Equipment Report",
            f"Filename: {dataset.filename}",
            f"Uploaded: {uploaded_at}",
            f"Total Records: {dataset.total_count}",
            f"Average Flowrate: {dataset.avg_flowrate:.2f}",
            f"Average Pressure: {dataset.avg_pressure:.2f}",
            f"Average Temperature: {dataset.avg_temperature:.2f}",
            "Equipment Type Distribution (Top 10):",
            *distribution_lines,
        ]

        pdf_bytes = _build_simple_pdf(lines)
        filename = f"equipment-report-{dataset.id}.pdf"
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class EquipmentViewSet(ReadOnlyModelViewSet):
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Equipment.objects.filter(dataset__user=self.request.user).order_by('-id')
