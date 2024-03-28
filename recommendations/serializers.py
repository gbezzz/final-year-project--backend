from rest_framework import serializers
from .models import Patient, Diagnose
from django.utils.timesince import timesince


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.CharField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "last_name",
            "first_name",
            "sex",
            "date_of_birth",
            "age",
            "phone_number",
            "email",
            "address",
        ]


class DiagnoseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Diagnose
        fields = [
            "patient",
            "doctor",
            "diagnosis_made",
            "doctor_name",
            "doctor_email",
            "doctor_phone",
            "created_at",
        ]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, %H:%M")


class ReportSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
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
