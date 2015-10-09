# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0002_auto_20151009_0041'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='challengedsegment',
            unique_together=set([('my_id', 'segment_id')]),
        ),
    ]
