from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, EquipmentViewSet

router = DefaultRouter()
router.register('datasets', DatasetViewSet, basename='dataset')
router.register('equipments', EquipmentViewSet, basename='equipment')
urlpatterns = router.urls
