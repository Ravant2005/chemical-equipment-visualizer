from django.urls import path
from .views import health_check, health_simple

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('', health_simple, name='health-simple'),
]