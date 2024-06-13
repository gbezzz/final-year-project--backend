from django.db import models

# from django.apps import apps
# from apps.get_model import Patient, Diagnosis  # Ensure this import is correct
from recommendations.models import Patient, Diagnosis

# from .model import Patient, Diagnosis  # Ensure this import is correct


# Create your models here.


# class History(models.Model):
#     patient = models.ForeignKey("recommendations.Patient", on_delete=models.CASCADE)
#     diagnosis = models.ForeignKey("recommendations.Diagnosis", on_delete=models.CASCADE)
#     diagnosis_made = models.TextField(default="")
#     selected_drug = models.CharField(max_length=100)
#     doctor_name = models.CharField(max_length=75, default="")
#     doctor_email = models.EmailField(default="")
#     doctor_phone = models.CharField(max_length=15, default="")
#     created_at = models.DateTimeField(auto_now_add=True, editable=False)

#     class Meta:
#         ordering = ["created_at"]

#     def __str__(self):
#         return f"Report for {self.diagnose.patient.first_name} {self.diagnose.patient.last_name} by Dr. {self.diagnose.doctor_name}"

# from django.db import models
# from patients.models import Patient
# from diagnosis.models import Diagnosis


class History(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    diagnosis_made = models.TextField()
    selected_drug = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=75)
    doctor_phone = models.CharField(max_length=15)
    doctor_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ["id"]

    def __str__(self):
        patient = models.ForeignKey("recommendations.Patient", on_delete=models.CASCADE)

        diagnosis = models.ForeignKey(
            "recommendations.Diagnosis", on_delete=models.CASCADE
        )
        # patient_instance = Patient.objects.get(pk=self.patient_id)
        # diagnosis_instance = Diagnosis.objects.get(pk=self.diagnosis_id)
        # return f"History of {self.patient.full_name()} by Dr. {self.doctor_name} with diagnosis: {self.diagnosis.diagnosis_made}"
        try:
            patient_instance = Patient.objects.get(pk=self.patient_id)
            diagnosis_instance = Diagnosis.objects.get(pk=self.diagnosis_id)
            return f"History of {patient_instance.full_name()} by Dr. {self.doctor_name} with diagnosis {diagnosis_instance.diagnosis_made}"
        except Patient.DoesNotExist:
            return "Unknown Patient"
        except Diagnosis.DoesNotExist:
            return "Unknown Diagnosis"

    @property
    def diagnose(self):
        return self.diagnosis.diagnosis_made
