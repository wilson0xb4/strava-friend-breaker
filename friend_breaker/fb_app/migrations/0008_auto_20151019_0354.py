# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0007_auto_20151019_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='newest_activity_date',
        ),
        migrations.RemoveField(
            model_name='athlete',
            name='oldest_activity_date',
        ),
    ]
