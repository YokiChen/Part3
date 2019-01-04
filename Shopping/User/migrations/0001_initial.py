# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-22 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rec',
            fields=[
                ('add_id', models.AutoField(primary_key=True, serialize=False)),
                ('rec_name', models.CharField(max_length=20)),
                ('rec_phone', models.CharField(max_length=20)),
                ('rec_country', models.CharField(max_length=15)),
                ('rec_pro', models.CharField(max_length=20)),
                ('rec_city', models.CharField(max_length=10)),
                ('rec_area', models.CharField(max_length=20)),
                ('rec_deta', models.CharField(max_length=40)),
            ],
            managers=[
                ('recmanage', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20)),
                ('user_pwd', models.CharField(max_length=20)),
                ('user_age', models.IntegerField()),
                ('user_header', models.ImageField(default='static/user/user1.jpg', null=True, upload_to='static/img/user_header/')),
                ('user_sex', models.CharField(max_length=5)),
                ('user_phone', models.CharField(max_length=14)),
            ],
            managers=[
                ('usermanage', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='rec',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Users'),
        ),
    ]
