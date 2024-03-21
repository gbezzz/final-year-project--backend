from rest_framework import serializers
from .models import Patient, Diagnose


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "last_name",
            "first_name",
            "sex",
            "age",
            "phone_number",
            "email",
            "address",
        ]


class DiagnoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnose
        fields = [
            "patient",
            "doctor",
            "diagnosis_made",
            "created_at",
        ]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, %H:%M")


class ReportSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor_name = serializers.CharField(source="doctor.get_full_name", read_only=True)
    doctor_phone = serializers.CharField(source="doctor.phone_number", read_only=True)
    doctor_email = serializers.EmailField(source="doctor.email", read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Diagnose
        fields = [
            "patient",
            "diagnosis_made",
            "doctor_name",
            "doctor_phone",
            "doctor_email",
            "created_at",
        ]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, %H:%M")
