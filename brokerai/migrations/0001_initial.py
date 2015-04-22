# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('symbol', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Predicted_data',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nn_daily', models.DecimalField(decimal_places=10, max_digits=15)),
                ('nn_weekly', models.DecimalField(decimal_places=10, max_digits=15)),
                ('nn_monthly', models.DecimalField(decimal_places=10, max_digits=15)),
                ('bs_daily', models.DecimalField(decimal_places=10, max_digits=15)),
                ('bs_weekly', models.DecimalField(decimal_places=10, max_digits=15)),
                ('bs_monthly', models.DecimalField(decimal_places=10, max_digits=15)),
                ('dt_daily', models.DecimalField(decimal_places=10, max_digits=15)),
                ('dt_weekly', models.DecimalField(decimal_places=10, max_digits=15)),
                ('dt_monthly', models.DecimalField(decimal_places=10, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Stock_data',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('open_price', models.DecimalField(decimal_places=10, max_digits=15)),
                ('low_price', models.DecimalField(decimal_places=10, max_digits=15)),
                ('high_price', models.DecimalField(decimal_places=10, max_digits=15)),
                ('close_price', models.DecimalField(decimal_places=10, max_digits=15)),
                ('volume', models.DecimalField(decimal_places=10, max_digits=15)),
                ('date', models.DateField()),
                ('currency', models.CharField(max_length=10)),
                ('company_id', models.ForeignKey(to='brokerai.Companies')),
            ],
        ),
        migrations.CreateModel(
            name='User_favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('company_id', models.ForeignKey(to='brokerai.Companies')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='user_favorite',
            name='user_id',
            field=models.ForeignKey(to='brokerai.Users'),
        ),
        migrations.AddField(
            model_name='predicted_data',
            name='stock_id',
            field=models.ForeignKey(to='brokerai.Stock_data'),
        ),
    ]
