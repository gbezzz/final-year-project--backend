from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_user_id(self, user_id, password):
        if user_id and password:
            user = self.authenticate(user_id=user_id, password=password)
        else:
            msg = _('Must include "user id" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
        )


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "phone_number",
        )

    def get_cleaned_data(self):
        super().__init__(self.data)
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

        user.save(
            update_fields=[
                "first_name",
                "last_name",
                "phone_number",
            ]
        )
        # group, created = Group.objects.get_or_create(name=user.role)
        # user.groups.add(group)
        return user
