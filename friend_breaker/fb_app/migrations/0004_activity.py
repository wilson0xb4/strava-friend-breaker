# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0003_auto_20151009_0247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('strava_id', models.IntegerField(serialize=False, primary_key=True)),
            ],
        ),
    ]
