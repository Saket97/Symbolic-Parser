# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-03 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_game_response4'),
    ]

    operations = [
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grammar', models.TextField(null=True)),
                ('parsetable', models.TextField(null=True)),
                ('firstset', models.TextField(null=True)),
                ('followset', models.TextField(null=True)),
            ],
        ),
    ]
