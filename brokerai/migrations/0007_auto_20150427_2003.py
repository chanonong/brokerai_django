# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brokerai', '0006_auto_20150427_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='predicted_data',
            name='bs_daily_recommend',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='predicted_data',
            name='bs_monthly_recommend',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='predicted_data',
            name='bs_weekly_recommend',
            field=models.BooleanField(default=False),
        ),
    ]
