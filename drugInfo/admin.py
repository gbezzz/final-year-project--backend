from django.contrib import admin
from .models import OrthodoxDrug, TraditionalDrug

# Register your models here.

class OrthodoxDrugAdmin(admin.ModelAdmin):
     list_display = (
        "name",
        "state",
        "manufacturers",
        "description",
     )

admin.site.register(OrthodoxDrug, OrthodoxDrugAdmin)

class TraditionalDrugAdmin(admin.ModelAdmin):
     list_display = (
        "name",
     )

admin.site.register(TraditionalDrug, TraditionalDrugAdmin)