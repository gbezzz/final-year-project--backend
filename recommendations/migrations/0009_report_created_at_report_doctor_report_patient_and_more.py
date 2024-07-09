# Generated by Django 4.0.10 on 2024-06-24 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommendations', '0008_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='doctor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='patient',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='recommendations.patient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='selected_drug',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='recommendations.traditionaldrug'),
            preserve_default=False,
        ),
    ]