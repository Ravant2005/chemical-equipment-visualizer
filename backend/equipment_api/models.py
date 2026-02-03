from django.db import models
from django.contrib.auth.models import User
import json

class Dataset(models.Model):
    """Model to store uploaded datasets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')
    
    # Summary statistics stored as JSON
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    equipment_distribution = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def summary(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'uploaded_at': self.uploaded_at.isoformat(),
            'total_count': self.total_count,
            'averages': {
                'flowrate': round(self.avg_flowrate, 2),
                'pressure': round(self.avg_pressure, 2),
                'temperature': round(self.avg_temperature, 2)
            },
            'equipment_distribution': self.equipment_distribution
        }

class Equipment(models.Model):
    """Model to store individual equipment records"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['equipment_name']
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
    
    @property
    def data(self):
        return {
            'id': self.id,
            'equipment_name': self.equipment_name,
            'type': self.equipment_type,
            'flowrate': self.flowrate,
            'pressure': self.pressure,
            'temperature': self.temperature
        }