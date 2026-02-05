from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from core.views import health_check, api_root

urlpatterns = [
    path("", api_root, name="api-root"),
    path("api/health/", csrf_exempt(health_check)),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/equipments/", include("equipments.urls")),
]

