from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet

# Router creates: /api/datasets/, /api/datasets/{id}/, etc.
router = DefaultRouter()
router.register('datasets', DatasetViewSet, basename='dataset')
urlpatterns = router.urls