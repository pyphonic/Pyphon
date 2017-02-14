# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 21:49
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, unique=True),
        ),
    ]
