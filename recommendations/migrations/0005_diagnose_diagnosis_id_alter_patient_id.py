# Generated by Django 4.0.10 on 2024-03-30 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0004_remove_patient_age_patient_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnose',
            name='diagnosis_id',
            field=models.CharField(default='none', max_length=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patient',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]