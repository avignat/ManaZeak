# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170929_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='CRC',
            field=models.CharField(default=0, max_length=1000),
            preserve_default=False,
        ),
    ]