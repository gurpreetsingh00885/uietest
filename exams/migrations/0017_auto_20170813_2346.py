# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 23:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0016_auto_20170813_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='selected_option',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.Option'),
        ),
    ]
