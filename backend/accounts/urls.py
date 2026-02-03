from django.urls import path
from .views import register, login

# Expose auth routes under the "auth/" prefix so when this module is
# included at the project root under "api/" the resulting paths are:
#   /api/auth/register/
#   /api/auth/login/
urlpatterns = [
    path('auth/register/', register, name='auth-register'),
    path('auth/login/', login, name='auth-login'),
]