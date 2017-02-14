# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 17:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=300)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('sender', models.CharField(choices=[('you', 'You'), ('them', 'Them')], max_length=12)),
            ],
        ),
    ]
