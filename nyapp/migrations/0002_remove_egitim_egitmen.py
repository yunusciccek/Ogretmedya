# Generated by Django 4.2.4 on 2023-09-04 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nyapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='egitim',
            name='egitmen',
        ),
    ]
