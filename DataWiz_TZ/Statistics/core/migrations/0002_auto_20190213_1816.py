# Generated by Django 2.1.5 on 2019-02-13 15:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchdate',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='searchdate',
            name='start_period',
            field=models.DateField(blank=True, default=datetime.date(2019, 2, 6)),
        ),
    ]
