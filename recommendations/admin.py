from django.contrib import admin

from drugInfo.admin import TraditionalDrugAdmin
from .models import Patient, Diagnosis, Report, TraditionalDrug

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


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "diagnosis_identifier",
        "diagnosis_made",
        "doctor_name",
        "doctor_email",
        "doctor_phone",
        "created_at",
    )


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "diagnosis",
        # "selected_orthodox_drug",
        # "selected_traditional_drug",
        "doctor",
        "created_at",
    )


class TraditionalDrugAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "disease_indications",
        "adverse_effects",
        "active_ingredient",
    )


admin.site.register(Patient, PatientAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(TraditionalDrug, TraditionalDrugAdmin)
