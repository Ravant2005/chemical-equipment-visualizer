from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from django.db import models
from .models import Dataset, Equipment
from .serializers import DatasetSerializer, DatasetDetailSerializer, EquipmentSerializer, UserSerializer
import pandas as pd
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user by deleting token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response(
            {'error': 'Something went wrong'},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current user info"""
    return Response(UserSerializer(request.user).data)

class DatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for Dataset operations"""
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return only user's datasets, limited to last 5
        return Dataset.objects.filter(user=self.request.user)[:5]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DatasetDetailSerializer
        return DatasetSerializer
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload and process CSV file"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # Validate file type
        if not file.name.endswith('.csv'):
            return Response(
                {'error': 'Only CSV files are allowed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV file
            df = pd.read_csv(file)
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate statistics
            total_count = len(df)
            avg_flowrate = df['Flowrate'].mean()
            avg_pressure = df['Pressure'].mean()
            avg_temperature = df['Temperature'].mean()
            
            # Get equipment type distribution
            equipment_distribution = df['Type'].value_counts().to_dict()
            
            # Create dataset
            file.seek(0)  # Reset file pointer
            dataset = Dataset.objects.create(
                user=request.user,
                filename=file.name,
                file=file,
                total_count=total_count,
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature,
                equipment_distribution=equipment_distribution
            )
            
            # Create equipment records
            equipment_records = []
            for _, row in df.iterrows():
                equipment_records.append(
                    Equipment(
                        dataset=dataset,
                        equipment_name=row['Equipment Name'],
                        equipment_type=row['Type'],
                        flowrate=row['Flowrate'],
                        pressure=row['Pressure'],
                        temperature=row['Temperature']
                    )
                )
            
            Equipment.objects.bulk_create(equipment_records)
            
            # Manage history (keep only last 5)
            user_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
            if user_datasets.count() > 5:
                # Delete oldest datasets
                datasets_to_delete = user_datasets[5:]
                for ds in datasets_to_delete:
                    ds.delete()
            
            return Response(
                DatasetDetailSerializer(dataset).data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': f'Error processing file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get summary statistics for a dataset"""
        dataset = self.get_object()
        
        return Response({
            'id': dataset.id,
            'filename': dataset.filename,
            'uploaded_at': dataset.uploaded_at,
            'total_count': dataset.total_count,
            'averages': {
                'flowrate': round(dataset.avg_flowrate, 2),
                'pressure': round(dataset.avg_pressure, 2),
                'temperature': round(dataset.avg_temperature, 2)
            },
            'equipment_distribution': dataset.equipment_distribution,
            'min_max': {
                'flowrate': {
                    'min': dataset.equipment.aggregate(min=models.Min('flowrate'))['min'],
                    'max': dataset.equipment.aggregate(max=models.Max('flowrate'))['max']
                },
                'pressure': {
                    'min': dataset.equipment.aggregate(min=models.Min('pressure'))['min'],
                    'max': dataset.equipment.aggregate(max=models.Max('pressure'))['max']
                },
                'temperature': {
                    'min': dataset.equipment.aggregate(min=models.Min('temperature'))['min'],
                    'max': dataset.equipment.aggregate(max=models.Max('temperature'))['max']
                }
            }
        })
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def generate_report(self, request, pk=None):
        """Generate PDF report for a dataset"""
        try:
            # Get dataset by ID and check ownership
            dataset = Dataset.objects.get(id=pk)
            
            # Simple token check
            token = request.GET.get('token') or request.META.get('HTTP_AUTHORIZATION', '').replace('Token ', '')
            if token:
                try:
                    from rest_framework.authtoken.models import Token
                    token_obj = Token.objects.get(key=token)
                    if dataset.user != token_obj.user:
                        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
                except Token.DoesNotExist:
                    return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Create PDF buffer
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
            
            # Container for the 'Flowable' objects
            elements = []
            
            # Define styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a365d'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2c5282'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title
            title = Paragraph("Chemical Equipment Analysis Report", title_style)
            elements.append(title)
            elements.append(Spacer(1, 0.3*inch))
            
            # Dataset Info
            info_style = styles['Normal']
            elements.append(Paragraph(f"<b>Dataset:</b> {dataset.filename}", info_style))
            elements.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))
            elements.append(Paragraph(f"<b>Total Equipment:</b> {dataset.total_count}", info_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # Summary Statistics
            elements.append(Paragraph("Summary Statistics", heading_style))
            
            summary_data = [
                ['Metric', 'Average Value'],
                ['Flowrate', f"{dataset.avg_flowrate:.2f}"],
                ['Pressure', f"{dataset.avg_pressure:.2f}"],
                ['Temperature', f"{dataset.avg_temperature:.2f}"]
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Equipment Distribution
            elements.append(Paragraph("Equipment Type Distribution", heading_style))
            
            # Safely handle equipment_distribution
            equipment_dist = dataset.equipment_distribution or {}
            if isinstance(equipment_dist, dict) and len(equipment_dist) > 0:
                dist_data = [['Equipment Type', 'Count']]
                for eq_type, count in equipment_dist.items():
                    dist_data.append([eq_type, str(count)])
            else:
                dist_data = [['Equipment Type', 'Count'], ['No data', '0']]
            
            dist_table = Table(dist_data, colWidths=[3*inch, 3*inch])
            dist_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(dist_table)
            elements.append(PageBreak())
            
            # Equipment Details
            elements.append(Paragraph("Equipment Details", heading_style))
            
            equipment_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
            for equipment in dataset.equipment.all():
                equipment_data.append([
                    equipment.equipment_name,
                    equipment.equipment_type,
                    f"{equipment.flowrate:.1f}",
                    f"{equipment.pressure:.1f}",
                    f"{equipment.temperature:.1f}"
                ])
            
            # Handle empty equipment list
            if len(equipment_data) == 1:
                equipment_data.append(['No equipment', '-', '-', '-', '-'])
            
            equipment_table = Table(equipment_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            equipment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8)
            ]))
            
            elements.append(equipment_table)
            
            # Build PDF
            doc.build(elements)
            
            # Get PDF value
            pdf = buffer.getvalue()
            buffer.close()
            
            # Create response
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
            
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get upload history (last 5 datasets)"""
        datasets = self.get_queryset()
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data)