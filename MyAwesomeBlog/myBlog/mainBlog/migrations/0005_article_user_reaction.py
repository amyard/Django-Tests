# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-12-17 21:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainBlog', '0004_auto_20181216_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='user_reaction',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
