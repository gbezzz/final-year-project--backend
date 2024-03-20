from django.contrib import admin
from .models import Patient, Diagnose

# Register your models here.
admin.site.register(Patient)
admin.site.register(Diagnose)
