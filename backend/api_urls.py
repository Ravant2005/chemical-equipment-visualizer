from django.urls import path, include

# Consolidated API routing - all API endpoints under /api/
urlpatterns = [
    path('', include('core.urls')),        # /api/health/
    path('', include('accounts.urls')),    # /api/auth/register/, /api/auth/login/  
    path('', include('equipments.urls')),  # /api/datasets/
]