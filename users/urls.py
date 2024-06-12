from django.urls import path
from .views import UserCreate, LoginView

urlpatterns = [
    path("register/", UserCreate.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
]
