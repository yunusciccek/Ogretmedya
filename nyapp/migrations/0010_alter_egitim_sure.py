# Generated by Django 4.2.5 on 2023-09-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nyapp', '0009_remove_egitim_baslik_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egitim',
            name='sure',
            field=models.PositiveIntegerField(help_text='Lütfen süreyi dakika cinsinden giriniz.'),
        ),
    ]
