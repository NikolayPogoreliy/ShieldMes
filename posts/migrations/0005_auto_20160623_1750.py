# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20160623_1439'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='posts',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='posts',
            name='level',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='posts',
            name='parent',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='posts.Posts'),
        ),
    ]