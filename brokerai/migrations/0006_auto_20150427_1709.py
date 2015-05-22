# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brokerai', '0005_auto_20150427_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='predicted_data',
            old_name='bs_daily',
            new_name='bs_daily_buy',
        ),
        migrations.RenameField(
            model_name='predicted_data',
            old_name='bs_monthly',
            new_name='bs_monthly_buy',
        ),
        migrations.RenameField(
            model_name='predicted_data',
            old_name='bs_weekly',
            new_name='bs_weekly_buy',
        ),
        migrations.AddField(
            model_name='predicted_data',
            name='bs_daily_sell',
            field=models.DecimalField(max_digits=15, decimal_places=10, null=True),
        ),
        migrations.AddField(
            model_name='predicted_data',
            name='bs_monthly_sell',
            field=models.DecimalField(max_digits=15, decimal_places=10, null=True),
        ),
        migrations.AddField(
            model_name='predicted_data',
            name='bs_weekly_sell',
            field=models.DecimalField(max_digits=15, decimal_places=10, null=True),
        ),
    ]
