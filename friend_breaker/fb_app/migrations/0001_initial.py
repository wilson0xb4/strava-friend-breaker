# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('strava_id', models.IntegerField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('newest_activity_date', models.CharField(max_length=20)),
                ('oldest_activity_date', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ChallenegedSegments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('my_id', models.IntegerField()),
                ('their_id', models.IntegerField()),
                ('their_name', models.CharField(max_length=50)),
                ('my_pr', models.IntegerField()),
                ('their_pr', models.IntegerField()),
                ('my_time', models.CharField(max_length=8)),
                ('their_time', models.CharField(max_length=8)),
                ('difference', models.CharField(max_length=8)),
                ('segment_id', models.IntegerField()),
                ('segment_name', models.CharField(max_length=200)),
                ('segment_distance', models.CharField(max_length=10)),
            ],
        ),
    ]
