# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 05:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=10)),
                ('department', models.CharField(choices=[('CS', 'Computer Science & Engineering'), ('IT', 'Information Technology'), ('BT', 'Biotechnology'), ('EC', 'Electronics and Communication Engineering'), ('EE', 'Electrical and Electronics Engineering'), ('ME', 'Mechanical Engineering')], max_length=50)),
                ('created', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Faculty Accounts',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('roll_no', models.CharField(max_length=8)),
                ('phone_no', models.CharField(max_length=10)),
                ('year', models.CharField(choices=[('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th')], max_length=1)),
                ('branch', models.CharField(choices=[('CS', 'Computer Science & Engineering'), ('IT', 'Information Technology'), ('BT', 'Biotechnology'), ('EC', 'Electronics and Communication Engineering'), ('EE', 'Electrical and Electronics Engineering'), ('ME', 'Mechanical Engineering')], max_length=2)),
                ('created', models.DateField(auto_now_add=True)),
                ('section', models.CharField(choices=[('1', 'A'), ('2', 'B')], max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Student Accounts',
            },
        ),
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('1', '1st'), ('2', '2nd'), ('3', '3rd'), ('4', '4th')], max_length=1)),
                ('branch', models.CharField(choices=[('CS', 'Computer Science & Engineering'), ('IT', 'Information Technology'), ('BT', 'Biotechnology'), ('EC', 'Electronics and Communication Engineering'), ('EE', 'Electrical and Electronics Engineering'), ('ME', 'Mechanical Engineering')], max_length=2)),
                ('section', models.CharField(choices=[('1', 'A'), ('2', 'B')], max_length=2)),
                ('number', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Study Groups',
            },
        ),
        migrations.AlterUniqueTogether(
            name='studygroup',
            unique_together=set([('number', 'section', 'year', 'branch')]),
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.StudyGroup'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
