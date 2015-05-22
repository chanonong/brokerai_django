# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('brokerai', '0002_auto_20150409_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_favorite',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='user_favorite',
            unique_together=set([('user_id', 'company_id')]),
        ),
    ]
