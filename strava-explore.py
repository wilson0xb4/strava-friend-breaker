"""
Exploring the Strava API through the
[stravalib](https://github.com/hozn/stravalib) library.
"""

from __future__ import unicode_literals
from __future__ import print_function
import os
from pprint import pprint

from stravalib.client import Client
from stravalib import unithelper

client_id = os.environ.get('STRAVA_CLIENT_ID', None)
client_secret = os.environ.get('STRAVA_CLIENT_SECRET', None)
access_token = os.environ.get('STRAVA_ACCESS_TOKEN', None)

if __name__ == '__main__':

    mysegments = {}

    # get athlete
    client = Client(access_token)
    athlete = client.get_athlete()

    # get athlete activities
    activities = client.get_activities(limit=1)

    # per activity, get segment efforts
    for activity in activities:
        segment_efforts = client.get_activity(activity.id).segment_efforts

        # per segment effort
        for segment in segment_efforts:
            mysegments[segment.segment.id] = segment.segment  # save to db

    # check if segment leaderboard contains any friends
    for key, segment in mysegments.iteritems():
        leaderboard = client.get_segment_leaderboard(key, following=True).entries

        # get friend with time < athlete time
        for person in leaderboard:
            if person.athlete_id == 1869056:
                me = person
                index = leaderboard.index(me)
                if index > 0:
                    other = leaderboard[index - 1]
                    data = {}
                    data['segment_name'] = segment.name
                    data['person_ahead'] = other.athlete_name
                    data['distance'] = str(unithelper.miles(segment.distance))
                    data['my_elapsed_time'] = str(me.elapsed_time)
                    # data['my_moving_time'] = str(me.moving_time)
                    data['their_elapsed_time'] = str(other.elapsed_time)
                    # data['their_moving_time'] = str(other.moving_time)
                    data['time_difference'] = str(me.elapsed_time - other.elapsed_time)
                    print('')
                    pprint(data)
