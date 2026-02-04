from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_view(request):
    """
    Health check endpoint for Railway deployment.
    MUST return 200 OK with JSON response.
    No database dependency to avoid startup issues.
    """
    return JsonResponse({"status": "ok"})