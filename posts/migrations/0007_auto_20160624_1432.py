# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-24 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20160624_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsmaxlevel',
            name='maxlevel',
            field=models.IntegerField(editable=False, null=True, verbose_name='Максимальный уровень вложенности для ветки'),
        ),
    ]
