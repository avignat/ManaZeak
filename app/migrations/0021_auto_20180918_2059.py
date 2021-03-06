# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-18 20:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0020_auto_20180602_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ViewColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('width', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='isPublic',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='playlistview',
            name='columns',
            field=models.ManyToManyField(to='app.ViewColumn'),
        ),
        migrations.AddField(
            model_name='playlistview',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Playlist'),
        ),
        migrations.AddField(
            model_name='playlistview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
