from django.db import models
from recommendations.models import Diagnose


# Create your models here.
class Report(models.Model):
    diagnose = models.ForeignKey(Diagnose, on_delete=models.CASCADE)
