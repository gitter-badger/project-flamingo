# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-20 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='read_at',
        ),
        migrations.AddField(
            model_name='message',
            name='recipient_deleted_perm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_deleted_perm',
            field=models.BooleanField(default=False),
        ),
    ]