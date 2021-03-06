# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-17 09:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_adminoptions_bufferpath'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.IntegerField(default=0)),
                ('expense', models.IntegerField(default=0)),
                ('loss', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='userpreferences',
            name='points',
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Wallet'),
        ),
    ]
