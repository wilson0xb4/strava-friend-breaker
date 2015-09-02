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

    # get athlete
    client = Client(access_token)
    athlete = client.get_athlete()

    # get athlete friends
    friends = athlete.friends
    for friend in friends:
        print(friend)

    # get athlete activities
    activity = client.get_activity(378663608)

    # per activity, get segment efforts
    # for activity in activities:
    print(activity)
    import pdb; pdb.set_trace()
    segments = activity.segment_efforts

    # per segment
    for segment in segments:
        print(segment)

        # check if segment is already tracked
        # check if segment leaderboard contains any friends
            # get friend with time < athlete time
