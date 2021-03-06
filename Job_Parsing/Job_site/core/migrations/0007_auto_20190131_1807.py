# Generated by Django 2.1.5 on 2019-01-31 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190130_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.CharField(max_length=70)),
                ('city', models.CharField(max_length=70)),
                ('site', models.CharField(max_length=70)),
                ('title', models.CharField(max_length=120)),
                ('url', models.URLField()),
                ('company', models.CharField(max_length=70)),
                ('date', models.CharField(max_length=70)),
            ],
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('number_id',)},
        ),
        migrations.AlterField(
            model_name='jobdescr',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
