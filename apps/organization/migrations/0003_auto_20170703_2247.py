# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20170703_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(default='', upload_to='org//%Y/%m', verbose_name='logo'),
        ),
    ]
