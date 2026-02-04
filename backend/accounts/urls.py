from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register, login

# These URLs are included under /api/ in main urls.py
# Final paths will be: /api/auth/register/, /api/auth/login/, etc.
urlpatterns = [
    path('auth/register/', register, name='auth-register'),
    path('auth/login/', login, name='auth-login'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]