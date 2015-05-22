# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brokerai', '0004_auto_20150427_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_daily',
            field=models.DecimalField(null=True, decimal_places=10, max_digits=15),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_monthly',
            field=models.DecimalField(null=True, decimal_places=10, max_digits=15),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_weekly',
            field=models.DecimalField(null=True, decimal_places=10, max_digits=15),
        ),
    ]
