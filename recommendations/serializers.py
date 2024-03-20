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
            "doctor_name",
            "doctor_email",
            "doctor_phone",
        ]


class ReportSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Diagnose
        fields = [
            "patient",
            "diagnosis_made",
            "doctor_name",
            "doctor_phone",
            "doctor_email",
        ]
