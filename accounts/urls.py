from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserDetail, LoginView, RegisterView

router = DefaultRouter()
router.register("accounts", UserViewSet, basename="accounts")


urlpatterns = [
    path("accounts/<int:pk>/", UserDetail.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
]
