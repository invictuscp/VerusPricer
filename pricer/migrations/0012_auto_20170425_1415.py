# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-25 14:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricer', '0011_caproductmatrix_dtiproductmatrix_fnproductmatrix_piproductmatrix'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fnproductmatrix',
            name='fico',
        ),
        migrations.RemoveField(
            model_name='fnproductmatrix',
            name='occupancy',
        ),
    ]