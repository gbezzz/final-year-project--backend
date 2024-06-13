from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrthodoxDrugViewSet, TraditionalDrugViewSet

router = DefaultRouter()
router.register(r"orthodox-drug", OrthodoxDrugViewSet, basename="orthodox-drug")
router.register(
    r"traditional-drug", TraditionalDrugViewSet, basename="traditional-drug"
)

urlpatterns = [
    path("", include(router.urls)),
]
