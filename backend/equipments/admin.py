from django.contrib import admin
from .models import Dataset, Equipment

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'total_count', 'uploaded_at']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'dataset']