# Generated by Django 4.0.10 on 2024-07-27 03:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0015_remove_report_selected_traditional_drug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vitals',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(250)])),
                ('temperature', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('systolic', models.IntegerField(blank=True, null=True)),
                ('diastolic', models.IntegerField(blank=True, null=True)),
                ('heart_rate', models.IntegerField(blank=True, null=True)),
                ('pulse_rhythm', models.CharField(blank=True, choices=[('regular', 'Regular'), ('irregular', 'Irregular')], max_length=10, null=True)),
                ('pulse_strength', models.CharField(blank=True, choices=[('strong', 'Strong'), ('weak', 'Weak')], max_length=10, null=True)),
                ('respiratory_rate', models.IntegerField(blank=True, null=True)),
                ('breathing_difficulty', models.BooleanField(default=False)),
                ('oxygen_saturation', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.RemoveField(
            model_name='patient',
            name='weight',
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='allergies',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='current_medications',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='extra_notes',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='medical_history',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='symptoms',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_details',
            field=models.CharField(default='null', max_length=250),
            preserve_default=False,
        ),
    ]
