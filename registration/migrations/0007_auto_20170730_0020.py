# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 00:20
from __future__ import unicode_literals

from django.db import migrations, models
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20170730_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='section',
            field=models.CharField(choices=[('A', '1'), ('B', '2')], default='A', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studygroup',
            name='section',
            field=models.CharField(choices=[('A', '1'), ('B', '2')], default='A', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='number',
            field=registration.models.IntegerRangeField(),
        ),
        migrations.AlterUniqueTogether(
            name='studygroup',
            unique_together=set([('number', 'section', 'year', 'branch')]),
        ),
    ]