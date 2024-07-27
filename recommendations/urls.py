from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    DiagnosisViewSet,
    ReportViewSet,
    VitalsViewSet,
    TradDrugAPIView,
)


router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"diagnosis", DiagnosisViewSet, basename="diagnosis")
router.register(r"reports", ReportViewSet, basename="reports")
router.register(r"vitals", VitalsViewSet, basename="vitals")



urlpatterns = [
    path("", include(router.urls)),
    path("trad-drugs/<str:pk>/", TradDrugAPIView.as_view(), name="trad_drugs"),
]
