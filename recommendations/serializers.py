from os import read
from pickle import TRUE
from rest_framework import serializers
from .models import Patient, Vitals, Diagnosis, Report, TraditionalDrug, OrthodoxDrug
from accounts.models import CustomUser
from accounts.serializers import UserSerializer
from rest_framework.exceptions import ValidationError 



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
            "phone_number",
            "email",
            "address",
        ]

    def get_age(self, obj) -> str:
        age = obj.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"

class VitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vitals
        fields = [
            "patient",
            "weight",
            "temperature",
            "systolic",
            "diastolic",
            "heart_rate",
            "pulse_rhythm",
            "pulse_strength",
            "respiratory_rate",
            "breathing_difficulty",
            "oxygen_saturation",
            "recorded_at",
            
        ]


class DiagnosisSerializer(serializers.ModelSerializer):
    diagnosis_identifier = serializers.CharField(read_only=TRUE)
    vitals = serializers.PrimaryKeyRelatedField(queryset=Vitals.objects.all())
    class Meta:
        model = Diagnosis
        fields = [
            "id",
            "patient",
            "doctor",
            "diagnosis_identifier",
            "vitals",
            "medical_history",
            "allergies",
            "symptoms",
            "current_medications",
            "diagnosis_made",
            "extra_notes",
            "created_at",
        ]
    

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y, %H:%M")


class TradDrugSerializer(serializers.ModelSerializer):
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
    diagnosis = serializers.PrimaryKeyRelatedField(queryset=Diagnosis.objects.all(), many=True)
    selected_orthodox_drug = serializers.PrimaryKeyRelatedField(
        queryset=OrthodoxDrug.objects.all(), many=True
    )
    selected_traditional_drug = serializers.PrimaryKeyRelatedField(
        queryset=TraditionalDrug.objects.all(), many=True
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "patient",
            "diagnosis",
            "selected_orthodox_drug",
            "selected_traditional_drug",
            "doctor",
            "created_at",
        ]
            
        


    def get_created_at(self, instance) -> str:
        return instance.created_at.strftime("%B %d, %Y, %H:%M")

    def get_patient_age(self, obj) -> str:
        age = obj.patient.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"

    def create(self, validated_data):
        diagnosis_data = validated_data.pop('diagnosis', [])
        selected_orthodox_drug_data = validated_data.pop('selected_orthodox_drug', [])
        selected_traditional_drug_data = validated_data.pop('selected_traditional_drug', [])

        report = Report.objects.create(**validated_data)

        if diagnosis_data:
            report.diagnosis.set(diagnosis_data)
        if selected_orthodox_drug_data:
            report.selected_orthodox_drug.set(selected_orthodox_drug_data)
        if selected_traditional_drug_data:
            report.selected_traditional_drug.set(selected_traditional_drug_data)

        return report

    def update(self, instance, validated_data):
        diagnosis_data = validated_data.pop('diagnosis', None)
        selected_orthodox_drug_data = validated_data.pop('selected_orthodox_drug', None)
        selected_traditional_drug_data = validated_data.pop('selected_traditional_drug', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if diagnosis_data is not None:
            instance.diagnosis.set(diagnosis_data)
        if selected_orthodox_drug_data is not None:
            instance.selected_orthodox_drug.set(selected_orthodox_drug_data)
        if selected_traditional_drug_data is not None:
            instance.selected_traditional_drug.set(selected_traditional_drug_data)

        instance.save()
        return instance