from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from allauth.account import app_settings as allauth_settings


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(
        max_length=8,
        required=True,
        allow_blank=False,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "user_id",
            "first_name",
            "last_name",
            "phone_number",
        )


# class CustomRegisterSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
#     first_name = serializers.CharField(max_length=30, required=True)
#     last_name = serializers.CharField(max_length=30, required=True)
#     phone_number = serializers.CharField(max_length=15, required=True)
#     password = serializers.CharField(write_only=True)
#     username = serializers.CharField(read_only=True)  # Add this line

#     def validate_email(self, email):
#         email = get_adapter().clean_email(email)
#         if allauth_settings.UNIQUE_EMAIL:
#             if email and email_address_exists(email):
#                 raise serializers.ValidationError(
#                     _("A user is already registered with this e-mail address."),
#                 )
#         return email

#     def validate_password(self, password):
#         return get_adapter().clean_password(password)

#     def get_cleaned_data(self):
#         return {
#             "first_name": self.validated_data.get("first_name", ""),
#             "last_name": self.validated_data.get("last_name", ""),
#             "phone_number": self.validated_data.get("phone_number", ""),
#             "password": self.validated_data.get("password", ""),
#             "email": self.validated_data.get("email", ""),
#             "username": self.validated_data.get("username", ""),  # And this line
#         }

#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         user = adapter.save_user(request, user, self, commit=False)
#         try:
#             adapter.clean_password(self.cleaned_data["password"], user=user)
#         except DjangoValidationError as exc:
#             raise serializers.ValidationError(
#                 detail=serializers.as_serializer_error(exc)
#             )
#         user.save()
#         setup_user_email(request, user, [])
#         return user


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if user is None:
                raise serializers.ValidationError(
                    "Invalid user_id/password combination."
                )
            if not user.is_active:
                raise serializers.ValidationError("User is deactivated.")
        else:
            raise serializers.ValidationError('Must include "user_id" and "password".')

        data["user"] = user
        return data


class CustomRegisterSerializer(RegisterSerializer):

    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "phone_number")

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).__init__(self.data)
        data_dict = super().get_cleaned_data()
        data_dict["first_name"] = self.validated_data.get("first_name", "")
        data_dict["last_name"] = self.validated_data.get("last_name", "")
        data_dict["phone_number"] = self.validated_data.get("phone_number", "")
        return data_dict

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.phone_number = self.cleaned_data.get("phone_number")
        user.save(update_fields=["first_name", "last_name", "phone_number"])
        return user
