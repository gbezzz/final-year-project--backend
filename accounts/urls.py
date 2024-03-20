from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserDetail

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("users/<int:pk>/", UserDetail.as_view()),
    path("", include(router.urls)),
]
