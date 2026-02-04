from django.http import HttpResponse


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

