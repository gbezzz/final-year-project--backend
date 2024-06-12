from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, LoginSerializer
from django.core.mail import send_mail
import random
import string
from rest_framework_simplejwt.authentication import JWTAuthentication

UserModel = get_user_model()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        user_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        user = serializer.save(user_id=user_id)
        send_mail(
            "Welcome",
            "Hello {}, your user id is {}".format(user.first_name, user.user_id),
            "from@example.com",
            [user.email],
            fail_silently=False,
        )


class LoginView(views.APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
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
