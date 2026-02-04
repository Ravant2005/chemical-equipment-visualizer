"""
Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from core.views import public_health_check

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Health check for deployment services like Railway
    path('health', public_health_check, name='public_health_check'),

    # API routes
    path('api/health/', include('core.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/equipments/', include('equipments.urls')),
]