# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0008_auto_20151019_0354'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='athlete',
            name='newest_activity_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='athlete',
            name='oldest_activity_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
