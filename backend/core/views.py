from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

@csrf_exempt
@never_cache
def health_check_view(request):
    """Minimal health check for Railway - no DB, no auth, no middleware dependencies"""
    return HttpResponse("OK", content_type="text/plain", status=200)