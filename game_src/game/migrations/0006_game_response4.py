# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20160523_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='Response4',
            field=models.TextField(null=True),
        ),
    ]
