from rest_framework import serializers
from .models import Patient, Diagnosis, Report, TraditionalDrug


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
    class Meta:
        model = Diagnosis
        fields = [
            "patient",
            "doctor",
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
    patient_id = serializers.CharField(source="patient.pid")
    patient_last_name = serializers.CharField(source="patient.last_name")
    patient_first_name = serializers.CharField(source="patient.first_name")
    patient_sex = serializers.CharField(source="patient.sex")
    patient_age = serializers.SerializerMethodField(source="patient.age")
    patient_phone_number = serializers.CharField(source="patient.phone_number")
    patient_email = serializers.EmailField(source="patient.email")
    patient_address = serializers.CharField(source="patient.address")
    diagnosis_identifier = serializers.CharField(
        source="diagnosis.diagnosis_identifier", read_only=True
    )
    diagnosis_made = serializers.CharField(source="diagnosis.diagnosis_made")
    selected_drug = serializers.CharField(source="diagnosis.selected_drug")
    doctor_name = serializers.CharField(source="doctor.get_full_name", read_only=True)
    doctor_phone = serializers.CharField(source="doctor.phone_number", read_only=True)
    doctor_email = serializers.EmailField(source="doctor.email", read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            "id",
            "patient_id",
            "patient_last_name",
            "patient_first_name",
            "patient_sex",
            "patient_age",
            "patient_phone_number",
            "patient_email",
            "patient_address",
            "diagnosis_identifier",
            "diagnosis_made",
            "selected_drug",
            "doctor_name",
            "doctor_phone",
            "doctor_email",
            "created_at",
        ]

    def create(self, validated_data):
        # Extract nested data
        patient_data = validated_data.pop('patient', None)
        diagnosis_data = validated_data.pop('diagnosis', None)

        # Create Diagnosis instance first
        diagnosis_instance = Diagnosis.objects.create(**diagnosis_data)

        # Now create Report instance
        report = Report.objects.create(
            patient=patient_data,
            diagnosis=diagnosis_instance,
            **validated_data
        )

        return report

    def get_created_at(self, instance) -> str:
        return instance.created_at.strftime("%B %d, %Y, %H:%M")

    def get_patient_age(self, obj) -> str:
        age = obj.patient.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"
