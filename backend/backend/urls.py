"""
Backend URL Configuration
Production-ready URL routing for Railway deployment.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def simple_health(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    # Health check for Railway (MANDATORY) - simple, no dependencies
    path('api/health/', simple_health),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/', include('accounts.urls')),
    path('api/', include('equipments.urls')),
]