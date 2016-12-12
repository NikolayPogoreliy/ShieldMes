# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 08:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='post_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='post_parent',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='post_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='post_title',
            new_name='title',
        ),
    ]
