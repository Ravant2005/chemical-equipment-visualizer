from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Public endpoint to verify that the API is running.
    """
    return Response({'status': 'ok', 'message': 'API is running'})

def public_health_check(request):
    """
    A simple health check endpoint that returns a JSON response.
    This is used by Railway's health checker.
    """
    return JsonResponse({"status": "ok"})