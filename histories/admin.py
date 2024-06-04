from django.contrib import admin
from .models import History


# Register your models here.
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "diagnosis",
        "patient",
        "diagnosis_made",
        "doctor_name",
        "doctor_email",
        "doctor_phone",
        "created_at",
    )


admin.site.register(History, HistoryAdmin)
