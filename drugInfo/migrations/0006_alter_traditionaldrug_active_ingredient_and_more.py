# Generated by Django 4.0.10 on 2024-05-09 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugInfo', '0005_alter_traditionaldrug_active_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Active_Ingredient',
            field=models.TextField(blank=True, default='Not Specified', null=True),
        ),
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Adverse_Effects',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Disease_Indications',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Product_Name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Scientific_Literature_Reference',
            field=models.TextField(blank=True, null=True),
        ),
    ]
