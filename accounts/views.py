from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters
from .models import CustomUser
from .serializers import UserSerializer, CustomLoginSerializer, CustomRegisterSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import generics

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
import random
import string
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import IntegrityError



# Create your views here.


class LoginView(generics.CreateAPIView):
    serializer_class = CustomLoginSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            user_id=serializer.validated_data["user_id"],
            password=serializer.validated_data["password"],
        )
        if user is not None:
            # login successful
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            # login failed
            return Response(
                {"message": "Invalid user_id or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

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


class RegisterView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(request=self.request)
        while True:
            user_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))  # generate a unique user_id
            if not CustomUser.objects.filter(user_id=user_id).exists():
                user.user_id = user_id
                try:
                    user.save()
                    break
                except IntegrityError:
                    continue
        send_mail(
            "Welcome",
            "Hello {}, your user id is {}".format(user.first_name, user.user_id),
            "from@example.com",
            [user.email],
            fail_silently=False,
        )

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return get_user_model().objects.all()
        else:
            return get_user_model().objects.filter(id=user.id)
