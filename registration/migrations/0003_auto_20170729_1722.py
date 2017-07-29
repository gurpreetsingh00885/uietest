# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 17:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20170726_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(choices=[('CS', 'Computer Science & Engineering'), ('IT', 'Information Technology'), ('BT', 'Biotechnology'), ('EC', 'Electronics and Communication Engineering'), ('EE', 'Electrical and Electronics Engineering'), ('ME', 'Mechanical Engineering')], max_length=2),
        ),
    ]
