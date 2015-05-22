# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brokerai', '0009_auto_20150427_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicted_data',
            name='bs_daily_recommend',
            field=models.IntegerField(),
        ),
    ]
