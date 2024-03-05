from django.contrib.auth import get_user_model
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
        ("nurse", "Nurse"),
        ("doctor", "Doctor"),
        ("lab", "Lab Personnel"),
        ("pharmacist", "Pharmacist"),
    )
    role = serializers.ChoiceField(choices=CHOICES)

    def get_cleaned_data(self):
        # Add this line
        super().__init__(self.data)

        # Add the following code
        data_dict = super().get_cleaned_data()
        data_dict["role"] = self.validated_data.get("role", "")
        return data_dict

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data.get("role")
        user.save()
        return user
