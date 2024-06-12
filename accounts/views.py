from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import generics
from dj_rest_auth.views import LoginView as BaseLoginView
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail

# Create your views here.


class LoginView(BaseLoginView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

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
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]


def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        email = user.email
        send_mail(
            "Welcome to Our Site",
            f"Your user ID is {user.id}",
            "from@example.com",
            [email],
            fail_silently=False,
        )
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.data["message"] = "Registration successful!"
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
