from django.urls import path
from .views import HealthCheckAPIView, ApiRootAPIView

urlpatterns = [
    path('', ApiRootAPIView.as_view(), name='api-root'),
    path('health/', HealthCheckAPIView.as_view(), name='health-check'),
]
