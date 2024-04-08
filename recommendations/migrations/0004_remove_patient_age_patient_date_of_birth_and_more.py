# Generated by Django 4.0.10 on 2024-03-28 18:31

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0003_diagnose_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='age',
        ),
        migrations.AddField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=20, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(250)]),
            preserve_default=False,
        ),
    ]
