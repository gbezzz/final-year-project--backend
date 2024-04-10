from django.db import models


class OrthodoxDrug(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    manufacturers = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        db_table = 'OrthodoxDrug'
        app_label = 'drugInfo'


def __str__(self):
    return f"Orthodox Drug"

class TraditionalDrug(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'TraditionalDrug'
        app_label = 'drugInfo'

def __str__(self):
    return f"Traditional Drug"