# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-23 15:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0021_auto_20180918_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistViewOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('randomMode', models.IntegerField(default=0)),
                ('repeatEnabled', models.IntegerField(default=0)),
                ('isActive', models.BooleanField(default=True)),
                ('columns', models.ManyToManyField(to='app.ViewColumn')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Playlist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ViewType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='playlistview',
            name='columns',
        ),
        migrations.RemoveField(
            model_name='playlistview',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='playlistview',
            name='user',
        ),
        migrations.DeleteModel(
            name='PlaylistView',
        ),
        migrations.AddField(
            model_name='playlistviewoptions',
            name='viewType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ViewType'),
        ),
    ]
