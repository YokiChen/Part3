# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-26 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Store', '0001_initial'),
        ('User', '0001_initial'),
        ('Goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('cart_good_num', models.IntegerField()),
                ('cart_single', models.IntegerField()),
                ('good_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Goods.Goods_mes')),
                ('store_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.Stores')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Users')),
            ],
            managers=[
                ('cartmanager', django.db.models.manager.Manager()),
            ],
        ),
    ]
