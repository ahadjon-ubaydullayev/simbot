# Generated by Django 3.0 on 2022-10-15 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='privacy_policy',
            field=models.BooleanField(default=False),
        ),
    ]