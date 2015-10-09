# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChallenegedSegments',
            new_name='ChallengedSegment',
        ),
        migrations.AlterField(
            model_name='athlete',
            name='newest_activity_date',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='oldest_activity_date',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
