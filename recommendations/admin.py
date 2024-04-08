from django.contrib import admin
from .models import Patient, Diagnose

# Register your models here.


# Register your models here.
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "sex",
        "display_age",
        "phone_number",
        "email",
        "address",
    )

    def display_age(self, obj):
        age = obj.age
        return f"{age['years']} years, {age['months']} months, and {age['days']} days"

    display_age.short_description = "Age"


class DiagnoseAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "diagnosis_id",
        "diagnosis_made",
        "doctor_name",
        "doctor_email",
        "doctor_phone",
        "created_at",
    )


admin.site.register(Patient, PatientAdmin)
admin.site.register(Diagnose, DiagnoseAdmin)
