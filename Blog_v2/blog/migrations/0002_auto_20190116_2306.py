# Generated by Django 2.1.5 on 2019-01-16 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-date_posted',)},
        ),
    ]
