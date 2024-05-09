# Generated by Django 4.0.10 on 2024-04-10 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0006_alter_diagnose_diagnosis_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnose',
            name='selected_drug',
            field=models.CharField(default='No drug selected at the time', max_length=100),
            preserve_default=False,
        ),
    ]