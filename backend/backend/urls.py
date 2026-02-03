from django.contrib import admin
from django.urls import path, include

# Root URL configuration - mount all app-level API routes under /api/
# Using explicit app includes avoids issues importing a separate
# top-level module in different deployment environments.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('equipments.urls')),
]