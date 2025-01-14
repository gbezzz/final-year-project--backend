# Generated by Django 4.0.10 on 2024-07-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0019_remove_report_diagnosis_report_diagnosis'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrthodoxDrug',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='report',
            name='selected_orthodox_drug',
        ),
        migrations.AddField(
            model_name='report',
            name='selected_orthodox_drug',
            field=models.ManyToManyField(to='recommendations.orthodoxdrug'),
        ),
    ]
