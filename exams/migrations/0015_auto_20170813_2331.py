# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 23:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0014_auto_20170813_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='exams.Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.CharField(choices=[('U', 'unanswered'), ('R', 'review'), ('L', 'locked'), ('N', 'not_visited')], default='U', max_length=20),
        ),
    ]
