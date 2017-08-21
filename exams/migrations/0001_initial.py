# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 05:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('U', 'unanswered'), ('R', 'review'), ('L', 'locked'), ('N', 'not_visited')], default='not_visited', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('is_correct', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('duration', models.DurationField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('groups', models.ManyToManyField(to='registration.StudyGroup')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='TestResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('submitted', models.BooleanField(default=False)),
                ('marks', models.IntegerField(default=0)),
                ('student', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='registration.Student')),
                ('test', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='exams.Test')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Test'),
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Question'),
        ),
        migrations.AddField(
            model_name='image',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='exams.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='exams.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='response',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='exams.TestResponse'),
        ),
        migrations.AddField(
            model_name='answer',
            name='selected_option',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exams.Option'),
        ),
    ]
