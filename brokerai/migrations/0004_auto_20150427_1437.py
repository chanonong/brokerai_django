# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brokerai', '0003_auto_20150425_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicted_data',
            name='bs_daily',
            field=models.DecimalField(decimal_places=10, null=True, max_digits=15),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='bs_monthly',
            field=models.DecimalField(decimal_places=10, null=True, max_digits=15),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='bs_weekly',
            field=models.DecimalField(decimal_places=10, null=True, max_digits=15),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_daily',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_monthly',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='dt_weekly',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='nn_daily',
            field=models.DecimalField(decimal_places=10, null=True, max_digits=15),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='nn_monthly',
            field=models.DecimalField(decimal_places=10, null=True, max_digits=15),
        ),
        migrations.AlterField(
            model_name='predicted_data',
            name='nn_weekly',
            field=models.DecimalField(decimal_places=10, null=True, max_digits=15),
        ),
    ]
