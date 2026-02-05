from django.http import HttpResponse, JsonResponse


def health_check(request):
    """
    Railway healthcheck endpoint - MUST be:
    - Fast (<50ms)
    - HTTP 200 only
    - GET-only
    - CSRF-exempt
    - Auth-free
    - No database queries
    - No external services
    """
    return HttpResponse("OK", status=200)


def api_root(request):
    """
    Root API view providing service information.
    """
    return JsonResponse(
        {"status": "ok", "service": "Chemical Equipment Backend", "version": "1.0"}
    )

