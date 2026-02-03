from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    """Simple healthcheck for Railway and other load-balancers.

    This endpoint must be publicly accessible so platform health checks
    (Railway, load balancers) receive HTTP 200 without authentication.
    """
    return Response({"status": "ok"})
