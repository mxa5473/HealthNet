# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-05-09 01:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meditems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='test',
            name='doc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Doctor'),
        ),
    ]