from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from allauth.account import app_settings as allauth_settings

# class LoginSerializer(serializers.Serializer):
#     user_id = serializers.CharField(max_length=8, required=True, allow_blank=False)
#     username = serializers.CharField(read_only=True)
#     email = serializers.EmailField(read_only=True)
#     password = serializers.CharField(style={"input_type": "password"})

#     class Meta:
#         model = get_user_model()
#         fields = ("user_id", "username", "email", "password")

#     def authenticate(self, **kwargs):
#         return authenticate(self.context["request"], **kwargs)

#     def _validate_email(self, email, password):
#         if email and password:
#             user = self.authenticate(email=email, password=password)
#         else:
#             msg = _('Must include "email" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def _validate_user_id(self, user_id, password):
#         if user_id and password:
#             user = self.authenticate(user_id=user_id, password=password)
#         else:
#             msg = _('Must include "user id" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def _validate_username_email(self, username, email, password):
#         if email and password:
#             user = self.authenticate(email=email, password=password)
#         elif username and password:
#             user = self.authenticate(username=username, password=password)
#         else:
#             msg = _('Must include either "username" or "email" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user
    


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=8, required=True, allow_blank=False, )
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "user_id",
            "first_name",
            "last_name",
            "phone_number",
        )


class CustomRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(write_only=True)
    user_id = serializers.CharField(read_only=True)  # Add this line

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'user_id': self.validated_data.get('user_id', ''),  # And this line
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
        user.save()
        setup_user_email(request, user, [])
        return user
    

class CustomLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_id = data.get('user_id')
        password = data.get('password')

        if user_id and password:
            user = authenticate(request=self.context.get('request'), user_id=user_id, password=password)

            if user is None:
                raise serializers.ValidationError('Invalid user_id/password combination.')
            if not user.is_active:
                raise serializers.ValidationError('User is deactivated.')
        else:
            raise serializers.ValidationError('Must include "user_id" and "password".')

        data['user'] = user
        return data