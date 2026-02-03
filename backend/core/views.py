from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class HealthCheckAPIView(APIView):
    """Public healthcheck endpoint for platform probes.

    Returns a minimal JSON body and HTTP 200. No authentication required.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})