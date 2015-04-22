# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brokerai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_daily',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_monthly',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_weekly',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='stock_data',
            name='volume',
            field=models.IntegerField(),
        ),
    ]
