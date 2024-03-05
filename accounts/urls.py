from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, UserDetail

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("users/<int:pk>/", UserDetail.as_view()),
    path("", include(router.urls)),
]
