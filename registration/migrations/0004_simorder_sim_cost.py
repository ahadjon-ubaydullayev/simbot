# Generated by Django 3.0 on 2022-11-28 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_simorder_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='simorder',
            name='sim_cost',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]