# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-22 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20160508_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='Response1',
            field=models.CharField(max_length=3, verbose_name='Response1'),
        ),
        migrations.AlterField(
            model_name='game',
            name='Response2',
            field=models.CharField(max_length=3, verbose_name='Response2'),
        ),
        migrations.AlterField(
            model_name='game',
            name='Response3',
            field=models.CharField(max_length=3, verbose_name='Response3'),
        ),
    ]
