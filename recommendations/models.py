from django.db import models
from accounts.models import CustomUser
from django.core.validators import MaxValueValidator
from histories.models import History
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Patient(models.Model):
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    SEX_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age = models.IntegerField(validators=[MaxValueValidator(150)])
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Diagnose(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    diagnosis_made = models.TextField()
    doctor_name = models.CharField(max_length=75)
    doctor_phone = models.CharField(max_length=15)
    doctor_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.doctor_name = f"{self.doctor.first_name} {self.doctor.last_name}"
        self.doctor_phone = f"{self.doctor.phone_number}"
        self.doctor_email = f"{self.doctor.email}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Diagnosis for {self.patient.first_name} {self.patient.last_name} by Dr. {self.doctor_name}"


# Signal to create a new History instance after a Diagnose instance is created
@receiver(post_save, sender=Diagnose)
def create_history(sender, instance, created, **kwargs):
    if created:
        History.objects.create(
            patient=instance.patient,
            diagnose=instance,
            diagnosis_made=instance.diagnosis_made,
            doctor_name=instance.doctor_name,
            doctor_email=instance.doctor_email,
            doctor_phone=instance.doctor_phone,
            created_at=instance.created_at,
        )
