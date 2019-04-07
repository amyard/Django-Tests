# Generated by Django 2.1.5 on 2019-04-06 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190406_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]