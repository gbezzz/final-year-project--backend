from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "gender",
            "role",
            "phone_number",
        )


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True)
    CHOICES = (
        ("admin", "Admin"),
        ("doctor", "Doctor"),
    )
    role = serializers.ChoiceField(choices=CHOICES, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "gender",
            "role",
        )

    def get_cleaned_data(self):
        super().__init__(self.data)
        data_dict = super().get_cleaned_data()
        data_dict["first_name"] = self.validated_data.get("first_name", "")
        data_dict["last_name"] = self.validated_data.get("last_name", "")
        data_dict["gender"] = self.validated_data.get("gender", "")
        data_dict["phone_number"] = self.validated_data.get("phone_number", "")
        data_dict["role"] = self.validated_data.get("role", "")
        return data_dict

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.gender = self.cleaned_data.get("gender")
        user.phone_number = self.cleaned_data.get("phone_number")
        user.role = self.cleaned_data.get("role")
        user.save(
            update_fields=["first_name", "last_name", "gender", "phone_number", "role"]
        )
        group, created = Group.objects.get_or_create(name=user.role)
        user.groups.add(group)
        return user
