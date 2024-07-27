# Generated by Django 4.0.10 on 2024-07-27 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0017_diagnosis_vitals'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitals',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recommendations.patient'),
            preserve_default=False,
        ),
    ]