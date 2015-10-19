# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0005_auto_20151019_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='start_count',
            field=models.IntegerField(default=0),
        ),
    ]
