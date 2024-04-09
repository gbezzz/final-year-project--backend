from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from dj_rest_auth.views import LoginView as BaseLoginView
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.


class LoginView(BaseLoginView):
    def get_response(self):
        original_response = super().get_response()
        refresh = RefreshToken.for_user(self.user)
        original_response.data["access"] = str(refresh.access_token)
        original_response.data["refresh"] = str(refresh)
        response.data["message"] = "Successfully Logged In!"
        # Remove the token created by dj-rest-auth automatically from the response
        if "key" in original_response.data:
            del original_response.data["key"]
        return original_response


class RegisterView(BaseRegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["message"] = "Registration successful!"
        # Remove the token created by dj-rest-auth automatically from the response
        if "key" in response.data:
            del response.data["key"]
        return response


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
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

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return get_user_model().objects.all()
        else:
            return get_user_model().objects.filter(id=user.id)

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
