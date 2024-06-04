# Generated by Django 4.0.10 on 2024-05-30 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugInfo', '0007_alter_orthodoxdrug_cas_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Active_Ingredient',
            field=models.CharField(blank=True, db_column='Active Ingredient', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Adverse_Effects',
            field=models.CharField(blank=True, db_column='Adverse Effects', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Disease_Indications',
            field=models.CharField(blank=True, db_column='Disease Indications', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='traditionaldrug',
            name='Product_Name',
            field=models.CharField(blank=True, db_column='Product Name', max_length=100, null=True),
        ),
    ]
