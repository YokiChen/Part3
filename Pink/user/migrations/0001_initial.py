# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-17 03:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', tinymce.models.HTMLField()),
                ('author', models.CharField(max_length=50)),
            ],
            managers=[
                ('addArt', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('header', models.ImageField(blank=True, default='static/img/header.jpg', null=True, upload_to='static/img/')),
            ],
            managers=[
                ('addStu', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
            ],
            managers=[
                ('useaddTea', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='teaid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher'),
        ),
        migrations.AddField(
            model_name='article',
            name='stuid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student'),
        ),
    ]
