# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import exams.models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0011_auto_20170812_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=exams.models.get_image_filename, verbose_name='Image')),
                ('question', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='exams.Question')),
            ],
        ),
    ]
