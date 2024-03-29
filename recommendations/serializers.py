from rest_framework import serializers
from .models import Patient, Diagnose


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
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

    def get_age(self, obj):
        age = obj.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"


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
    patient_id = serializers.CharField(source="patient.patient_id")
    patient_last_name = serializers.CharField(source="patient.last_name")
    patient_first_name = serializers.CharField(source="patient.first_name")
    patient_sex = serializers.CharField(source="patient.sex")
    patient_age = serializers.SerializerMethodField(source="patient.age")
    patient_phone_number = serializers.CharField(source="patient.phone_number")
    patient_email = serializers.EmailField(source="patient.email")
    patient_address = serializers.CharField(source="patient.address")
    doctor_name = serializers.CharField(source="doctor.get_full_name", read_only=True)
    doctor_phone = serializers.CharField(source="doctor.phone_number", read_only=True)
    doctor_email = serializers.EmailField(source="doctor.email", read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Diagnose
        fields = [
            "patient_id",
            "patient_last_name",
            "patient_first_name",
            "patient_sex",
            "patient_age",
            "patient_phone_number",
            "patient_email",
            "patient_address",
            "diagnosis_made",
            "doctor_name",
            "doctor_phone",
            "doctor_email",
            "created_at",
        ]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, %H:%M")

    def get_patient_age(self, obj):
        age = obj.patient.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"
