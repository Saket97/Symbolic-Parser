# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Response1', models.CharField(max_length=1)),
                ('Response2', models.CharField(max_length=1)),
                ('Response3', models.CharField(max_length=3)),
            ],
        ),
    ]
