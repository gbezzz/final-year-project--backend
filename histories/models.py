from django.db import models


# Create your models here.


class History(models.Model):
    patient = models.ForeignKey("recommendations.Patient", on_delete=models.CASCADE)
    diagnose = models.ForeignKey("recommendations.Diagnose", on_delete=models.CASCADE)
    diagnosis_made = models.TextField(default="")
    doctor_name = models.CharField(max_length=75, default="")
    doctor_email = models.EmailField(default="")
    doctor_phone = models.CharField(max_length=15, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.diagnose.patient.first_name} {self.diagnose.patient.last_name} by Dr. {self.diagnose.doctor_name}"
