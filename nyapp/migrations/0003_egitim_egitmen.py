# Generated by Django 4.2.4 on 2023-09-04 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nyapp', '0002_remove_egitim_egitmen'),
    ]

    operations = [
        migrations.AddField(
            model_name='egitim',
            name='egitmen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
