# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-31 12:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20180129_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='name',
        ),
        migrations.RemoveField(
            model_name='library',
            name='user',
        ),
    ]