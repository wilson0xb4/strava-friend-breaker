# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0009_auto_20151019_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengedsegment',
            name='difference',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='challengedsegment',
            name='my_time',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='challengedsegment',
            name='their_time',
            field=models.CharField(max_length=15),
        ),
    ]
