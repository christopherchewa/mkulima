# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-12 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170212_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_phonenumber',
            field=models.CharField(max_length=10),
        ),
    ]
