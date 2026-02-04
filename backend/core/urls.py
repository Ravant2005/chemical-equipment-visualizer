from django.urls import path
from .views import health_check_view

urlpatterns = [
    path('', health_check_view, name='health_check'),
]
