from django.db import models
from accounts.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.core.validators import MaxValueValidator
import string
import random

# Create your models here.


class Patient(models.Model):
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    id = models.AutoField(primary_key=True)

    @property
    def pid(self):
        return "PID" + str(self.id).zfill(7)

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)

    SEX_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField()

    @property
    def age(self):
        today = date.today()
        years = (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
        months = (
            today.month
            - self.date_of_birth.month
            - (today.day < self.date_of_birth.day)
        ) % 12
        days = (today.day - self.date_of_birth.day) % 30  # This is an approximation
        return {"years": years, "months": months, "days": days}


    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    emergency_contact_details = models.CharField(max_length=250)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Vitals(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
    )

    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    systolic = models.IntegerField( null=True, blank=True)
    diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    pulse_rhythm = models.CharField(max_length=10, choices=[('regular', 'Regular'), ('irregular', 'Irregular')], null=True, blank=True)
    pulse_strength = models.CharField(max_length=10, choices=[('strong', 'Strong'), ('weak', 'Weak')], null=True, blank=True)
    respiratory_rate = models.IntegerField(null=True, blank=True)
    breathing_difficulty = models.BooleanField(default=False)
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Patient Vitals"

class Diagnosis(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    

    def generate_diagnosis_identifier(self):
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return "".join(random.choice(characters) for _ in range(8))

    diagnosis_identifier = models.CharField(max_length=8, unique=True)
    vitals = models.ForeignKey(Vitals, on_delete=models.CASCADE)
    medical_history = models.TextField()
    allergies = models.TextField()
    symptoms = models.TextField()
    current_medications = models.TextField()
    extra_notes = models.TextField()
    diagnosis_made = models.TextField()
    doctor_name = models.CharField(max_length=75)
    doctor_phone = models.CharField(max_length=15)
    doctor_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.doctor_name = f"{self.doctor.first_name} {self.doctor.last_name}"
        self.doctor_phone = f"{self.doctor.phone_number}"
        self.doctor_email = f"{self.doctor.email}"
        if not self.diagnosis_identifier:
            self.diagnosis_identifier = self.generate_diagnosis_identifier()
            while Diagnosis.objects.filter(
                diagnosis_identifier=self.diagnosis_identifier
            ).exists():
                self.diagnosis_identifier = self.generate_diagnosis_identifier()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Diagnosis for {self.patient.first_name} {self.patient.last_name} by Dr. {self.doctor_name}: {self.diagnosis_made}"


class OrthodoxDrug(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name

class TraditionalDrug(models.Model):

    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=1000, null=True)
    active_ingredient = models.CharField(max_length=1000, null=True)
    disease_indications = models.CharField(max_length=1000, null=True)
    scientific_literature_reference = models.CharField(max_length=1000, null=True)
    adverse_effects = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.product_name


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    diagnosis = models.ManyToManyField(Diagnosis)
    selected_orthodox_drug = models.ManyToManyField(OrthodoxDrug)
    selected_traditional_drug = models.ManyToManyField(TraditionalDrug)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.diagnosis.patient.first_name} {self.diagnosis.patient.last_name} by Dr. {self.diagnosis.doctor_name} on {self.created_at.strftime('%Y-%m-%d')}"


