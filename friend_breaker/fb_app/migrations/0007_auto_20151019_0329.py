# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_app', '0006_auto_20151019_0323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='athlete',
            old_name='start_count',
            new_name='home_coord_count',
        ),
        migrations.RenameField(
            model_name='athlete',
            old_name='start_lat_est',
            new_name='home_lat',
        ),
        migrations.RenameField(
            model_name='athlete',
            old_name='start_long_est',
            new_name='homt_long',
        ),
    ]
