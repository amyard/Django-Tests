# Generated by Django 2.1.5 on 2019-04-09 17:53

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_auto_20190407_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user_reaction',
        ),
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='user_reaction_dislikes',
            field=models.ManyToManyField(blank=True, related_name='user_reaction_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='user_reaction_likes',
            field=models.ManyToManyField(blank=True, related_name='user_reaction_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comments',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 9, 17, 53, 41, 628734)),
        ),
    ]
