from __future__ import absolute_import

from celery import shared_task

from stravalib import Client, unithelper

from .models import Athlete, Activity, ChallengedSegment

@shared_task
def get_activity_list():
    pass


@shared_task
def get_activity():
    pass


@shared_task
def get_segment_efforts():
    pass


@shared_task
def get_leaderboard():
    pass


@shared_task
def massive_test(access_token, athlete_id):
    client = Client(access_token=access_token)

    mysegments = {}  # all segments a user has ridden

    # get athlete activities
    athlete_from_db = Athlete.objects.get(strava_id=athlete_id)
    activities = client.get_activities(limit=5, before=athlete_from_db.oldest_activity_date)  # API call

    # per activity, get segment efforts
    for activity in activities:
        if activity.type not in ['Ride', 'ride']:
            continue

        try:
            # if activity already exists in db, skip it
            Activity.objects.get(strava_id=activity.id)
            continue
        except Activity.DoesNotExist:
            new_activity = Activity()
            new_activity.strava_id = activity.id
            new_activity.start_lat = activity.start_latitude
            new_activity.start_long = activity.start_longitude
            new_activity.start_date = activity.start_date
            new_activity.save()

            # update newest / oldest activity dates
            if athlete_from_db.newest_activity_date is None:
                athlete_from_db.newest_activity_date = activity.start_date
                athlete_from_db.oldest_activity_date = activity.start_date
            else:
                if activity.start_date > athlete_from_db.newest_activity_date:
                    athlete_from_db.newest_activity_date = activity.start_date
                elif activity.start_date < athlete_from_db.oldest_activity_date:
                    athlete_from_db.oldest_activity_date = activity.start_date
            athlete_from_db.save()

        segment_efforts = client.get_activity(activity.id).segment_efforts   # API call

        # per segment effort
        for segment in segment_efforts:
            mysegments[segment.segment.id] = segment.segment  # save to db

    # check if segment leaderboard contains any friends
    for key, segment in mysegments.iteritems():
        leaderboard = client.get_segment_leaderboard(key, following=True).entries   # API call (possibly lots, depends on number of segments)

        # get friend with time < athlete time
        for i, entry in enumerate(leaderboard):
            if entry.athlete_id == athlete_id:
                me = entry

                if i == 0:
                    # I'm already the winner!
                    break

                j = 1
                while j <= i and leaderboard[i - j].elapsed_time == me.elapsed_time:
                    # check for ties, compare each entry from i to zero (possibly)
                    j += 1
                if leaderboard[i - j].elapsed_time == me.elapsed_time:
                    # if they're still tied at the end of the loop, I don't want to see it
                    break

                other = leaderboard[i - j]

                try:
                    new_segment = ChallengedSegment.objects.get(my_id=athlete_id, segment_id=segment.id)
                except ChallengedSegment.DoesNotExist:
                    new_segment = ChallengedSegment()

                new_segment.my_id = athlete_id
                new_segment.their_id = other.athlete_id
                new_segment.their_name = other.athlete_name

                new_segment.my_pr = me.activity_id
                new_segment.their_pr = other.activity_id

                new_segment.my_time = str(me.elapsed_time)
                new_segment.their_time = str(other.elapsed_time)
                new_segment.difference = str(me.elapsed_time - other.elapsed_time)

                new_segment.segment_id = segment.id
                new_segment.segment_name = segment.name
                new_segment.segment_distance = str(unithelper.miles(segment.distance))
                new_segment.save()

                break  # we already found my entry, why keep looking through the list?
