from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DiagnoseViewSet, ReportViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet)
router.register(r"diagnoses", DiagnoseViewSet)
router.register(r"reports", ReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
