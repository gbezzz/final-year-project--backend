from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters
from .models import CustomUser
from .serializers import UserSerializer, CustomLoginSerializer, CustomRegisterSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from allauth.account import app_settings as allauth_settings
from django.conf import settings
from dj_rest_auth.app_settings import (
    JWTSerializer,
    TokenSerializer,
    create_token,
)
from dj_rest_auth.models import TokenModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
import random
import string
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from django.db import IntegrityError
from dj_rest_auth.views import LoginView as BaseLoginView
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView

# Create your views here.


class LoginView(BaseLoginView):
    def get_response(self):
        original_response = super().get_response()
        refresh = RefreshToken.for_user(self.user)
        original_response.data["access"] = str(refresh.access_token)
        original_response.data["refresh"] = str(refresh)
        original_response.data["message"] = "Successfully Logged In!"
        # Remove the token created by dj-rest-auth automatically from the response
        if "key" in original_response.data:
            del original_response.data["key"]
        return original_response


class RegisterView(BaseRegisterView):
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        username = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        user.username = username
        try:
            user.save()
        except IntegrityError:
            pass
        # if getattr(settings, "REST_USE_JWT", False):
        #     self.access_token, self.refresh_token = jwt_encode(user)
        # else:
        create_token(self.token_model, user, serializer)
        return user

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["message"] = "Registration successful!"
        # Remove the token created by dj-rest-auth automatically from the response
        if "key" in response.data:
            del response.data["key"]
        return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    # authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "first_name",
        "last_name",
        "phone_number",
    ]


class UserDetail(generics.RetrieveDestroyAPIView):
    queryset = get_user_model().objects.all()
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return get_user_model().objects.all()
        else:
            return get_user_model().objects.filter(id=user.id)
