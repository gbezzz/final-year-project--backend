from rest_framework import serializers
from .models import History


class HistorySerializer(serializers.ModelSerializer):
    patient_id = serializers.CharField(source="patient.pid")
    patient_last_name = serializers.CharField(source="patient.last_name")
    patient_first_name = serializers.CharField(source="patient.first_name")
    patient_sex = serializers.CharField(source="patient.sex")
    patient_age = serializers.SerializerMethodField(source="patient.age")
    patient_phone_number = serializers.CharField(source="patient.phone_number")
    patient_email = serializers.EmailField(source="patient.email")
    patient_address = serializers.CharField(source="patient.address")
    diagnosis_id = serializers.CharField(source="diagnose.diagnosis_id")

    class Meta:
        model = History
        fields = [
            "patient",
            "patient_id",
            "patient_last_name",
            "patient_first_name",
            "patient_sex",
            "patient_age",
            "patient_phone_number",
            "patient_email",
            "patient_address",
            "diagnose",
            "diagnosis_id",
            "diagnosis_made",
            "doctor_name",
            "doctor_email",
            "doctor_phone",
            "created_at",
        ]

    def get_patient_detail(self, obj):
        return str(obj.patient)

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, %H:%M")

    def get_patient_age(self, obj) -> str:
        age = obj.patient.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"
