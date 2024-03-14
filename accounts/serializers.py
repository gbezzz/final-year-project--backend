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
            "name",
            "role",
        )


class CustomRegisterSerializer(RegisterSerializer):
    CHOICES = (
        ("admin", "Admin"),
        ("doctor", "Doctor"),
    )
    role = serializers.ChoiceField(choices=CHOICES)

    def get_cleaned_data(self):
        super().__init__(self.data)
        data_dict = super().get_cleaned_data()
        data_dict["role"] = self.validated_data.get("role", "")
        return data_dict

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data.get("role")
        user.save(update_fields=["role"])
        group, created = Group.objects.get_or_create(name=user.role)
        user.groups.add(group)
        return user
