# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0004_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='start_lat',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='start_long',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='athlete',
            name='start_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='athlete',
            name='start_lat_est',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='athlete',
            name='start_long_est',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
