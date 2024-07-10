from os import read
from pickle import TRUE
from rest_framework import serializers
from .models import Patient, Diagnosis, Report, TraditionalDrug
from accounts.models import CustomUser
from accounts.serializers import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    patient_id = serializers.CharField(source="pid", read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "patient_id",
            "last_name",
            "first_name",
            "sex",
            "date_of_birth",
            "age",
            "weight",
            "phone_number",
            "email",
            "address",
        ]

    def get_age(self, obj) -> str:
        age = obj.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"


class DiagnosisSerializer(serializers.ModelSerializer):
    diagnosis_identifier = serializers.CharField(read_only=TRUE)

    class Meta:
        model = Diagnosis
        fields = [
            "id",
            "patient",
            "doctor",
            "diagnosis_identifier",
            "diagnosis_made",
            "created_at",
        ]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, %H:%M")


class TraditionalDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraditionalDrug
        fields = [
            "id",
            "product_name",
            "disease_indications",
            "adverse_effects",
            "active_ingredient",
        ]


class ReportSerializer(serializers.ModelSerializer):

    selected_drug = serializers.PrimaryKeyRelatedField(
        queryset=TraditionalDrug.objects.all()
    )

    class Meta:
        model = Report
        fields = (
            "id",
            "patient",
            "diagnosis",
            "selected_drug",
            "doctor",
            "created_at",
        )

    def get_created_at(self, instance) -> str:
        return instance.created_at.strftime("%B %d, %Y, %H:%M")

    def get_patient_age(self, obj) -> str:
        age = obj.patient.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"
