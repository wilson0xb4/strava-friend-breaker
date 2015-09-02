"""
Exploring the Strava API through the
[stravalib](https://github.com/hozn/stravalib) library.
"""

from __future__ import unicode_literals
from __future__ import print_function
import os

from stravalib.client import Client

client_id = os.environ.get('STRAVA_CLIENT_ID', None)
client_secret = os.environ.get('STRAVA_CLIENT_SECRET', None)
access_token = os.environ.get('STRAVA_ACCESS_TOKEN', None)

if __name__ == '__main__':
    pass
