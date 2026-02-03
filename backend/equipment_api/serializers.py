from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, Equipment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class DatasetSerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'uploaded_at', 'total_count', 'avg_flowrate', 
                  'avg_pressure', 'avg_temperature', 'equipment_distribution', 'equipment_count']
        read_only_fields = ['uploaded_at', 'total_count', 'avg_flowrate', 
                           'avg_pressure', 'avg_temperature', 'equipment_distribution']
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()

class DatasetDetailSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'uploaded_at', 'total_count', 'avg_flowrate', 
                  'avg_pressure', 'avg_temperature', 'equipment_distribution', 'equipment']