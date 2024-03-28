from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DiagnoseViewSet, ReportViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"diagnoses", DiagnoseViewSet, basename="diagnoses")
router.register(r"reports", ReportViewSet, basename="reports")

urlpatterns = [
    path("", include(router.urls)),
]
