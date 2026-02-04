"""
Backend URL Configuration
Production-ready URL routing for Railway deployment.
"""
from django.contrib import admin
from django.urls import path, include
from core.views import health_check_view

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Health check for Railway (MANDATORY)
    path('api/health/', health_check_view, name='health_check'),
    
    # API routes - single canonical root
    path('api/', include('accounts.urls')),
    path('api/', include('equipments.urls')),
]