from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    DiagnosisViewSet,
    ReportViewSet,
    RecommendTradDrugsView,
    TradDrugAPIView,
)


router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"diagnosis", DiagnosisViewSet, basename="diagnosis")
# router.register(r"trad-drugs", TradDrugViewSet, basename="trad-drugs")
router.register(r"reports", ReportViewSet, basename="reports")


urlpatterns = [
    # path("", include(router.urls)),
    # path(
    #     "api/recommendations/",
    #     RecommendTradDrugView.as_view(),
    #     name="recommend-trad-drugs",
    # ),
    # other paths...
    path("recommender/", RecommendTradDrugsView.as_view(), name="recommender"),
    path("trad-drugs/<str:pk>/", TradDrugAPIView.as_view(), name="trad_drugs"),
]
