from django.contrib import admin
from django.urls import path, include
from core.views import health_check

urlpatterns = [
    path("api/health/", health_check),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/equipments/", include("equipments.urls")),
]