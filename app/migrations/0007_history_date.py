# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-09 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_history_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
