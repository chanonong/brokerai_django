# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brokerai', '0007_auto_20150427_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicted_data',
            name='bs_monthly_recommend',
            field=models.BooleanField(),
        ),
    ]
