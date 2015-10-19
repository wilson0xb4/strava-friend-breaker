from __future__ import unicode_literals
from __future__ import print_function
import os

from django.shortcuts import render, redirect
from stravalib import Client
from stravalib import unithelper

from models import Athlete, Activity, ChallengedSegment


def index(request):
    access_token = request.session.get('access_token', None)
    if access_token is None:
        # if access_token is NOT in session, kickoff the oauth exchange
        client = Client()
        url = client.authorization_url(
            client_id=os.environ.get('STRAVA_CLIENT_ID', None),
            redirect_uri='http://127.0.0.1:8000/authorization'
        )
        context = {'auth_url': url}
        return render(request, 'index.html', context)

    # otherwise, load authorized user
    client = Client(access_token=access_token)

    athlete_id = request.session.get('athlete_id', None)
    if athlete_id is None:
        # if athlete is NOT already in session, get athlete
        # (attempting to reduce calls to the API)
        athlete = client.get_athlete()
        request.session['athlete_id'] = athlete.id
        request.session['firstname'] = athlete.firstname

        try:
            Athlete.objects.get(strava_id=athlete.id)
        except Athlete.DoesNotExist:
            new_athlete = Athlete()
            new_athlete.strava_id = athlete.id
            new_athlete.first_name = athlete.firstname
            new_athlete.last_name = athlete.lastname
            new_athlete.city = athlete.city
            new_athlete.state = athlete.state
            new_athlete.country = athlete.country
            new_athlete.save()

    return render(request, 'welcome_landing.html')


def _build_context(client, athlete_id):
    context = {}
    segments = {}  # segments with with a faster friend
    mysegments = {}  # all segments a user has ridden

    # get athlete activities
    athlete_from_db = Athlete.objects.get(strava_id=athlete_id)
    activities = client.get_activities(limit=5)  # API call

    # per activity, get segment efforts
    for activity in activities:
        try:
            # if activity already exists in db, skip it
            Activity.objects.get(strava_id=activity.id)
            continue
        except Activity.DoesNotExist:
            new_activity = Activity()
            new_activity.strava_id = activity.id
            new_activity.start_lat = activity.start_latitude
            new_activity.start_long = activity.start_longitude
            new_activity.save()

            # update users 'home' location estimate
            # move somewhere else, run after a user has x rides loaded (initial case of loading initial ride is not accounted for currently)
            # athlete_from_db.home_coord_count += 1
            # athlete_from_db.home_lat = (athlete_from_db.home_lat + activity.start_latitude) / athlete_from_db.home_coord_count
            # athlete_from_db.home_long = (athlete_from_db.home_long + activity.start_longitude) / athlete_from_db.home_coord_count
            # athlete_from_db.save()

        segment_efforts = client.get_activity(activity.id).segment_efforts   # API call

        # per segment effort
        for segment in segment_efforts:
            mysegments[segment.segment.id] = segment.segment  # save to db

    # count = 0  # for testing, limit segments

    # check if segment leaderboard contains any friends
    for key, segment in mysegments.iteritems():
        leaderboard = client.get_segment_leaderboard(key, following=True).entries   # API call (possibly lots, depends on number of segments)

        # limit the segments while testing
        # count += 1
        # if count > 10:
        #     break

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

                segments[segment.name] = {}
                segments[segment.name]['segment_name'] = segment.name
                segments[segment.name]['segment_id'] = segment.id
                segments[segment.name]['challenger_name'] = other.athlete_name
                segments[segment.name]['challenger_id'] = other.athlete_id
                segments[segment.name]['my_pr_id'] = me.activity_id
                segments[segment.name]['their_pr_id'] = other.activity_id
                segments[segment.name]['my_elapsed_time'] = str(me.elapsed_time)
                segments[segment.name]['their_elapsed_time'] = str(other.elapsed_time)
                segments[segment.name]['time_difference'] = str(me.elapsed_time - other.elapsed_time)
                segments[segment.name]['distance'] = str(unithelper.miles(segment.distance))

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

    context['segments'] = segments
    return context


def update(request):
    '''
    Kickoff the update process!

    Initially:
        grab most recent ride and look at those segments.
    Eventually...
        Starts the background process that will analyze every ride and
        every segment a user has ridden.
    '''

    # check that I have both an `access_token` and an `athlete_id`
    # essentially, "is the user logged in"
    if not request.session.get('access_token', False) and request.session.get('athlete_id', False):
        # could redirect 401 or 403 instead...but just put them at the home page
        return redirect(index)

    client = Client(access_token=request.session.get('access_token', None))
    athlete_id = request.session.get('athlete_id', None)

    context = _build_context(client, athlete_id)

    # return render(request, 'index_loggedin.html', context)
    return redirect(challenged_segments, athlete=athlete_id)


def challenged_segments(request, athlete):
    segments = ChallengedSegment.objects.filter(my_id=athlete)

    context = {}
    context['segments'] = segments
    return render(request, 'index_loggedin.html', context)


def authorization(request):
    '''
    Trades in the `code` sent from Strava for an `access_token`.
    Ties that `access_token` to a users session.
    '''

    code = request.GET.get('code', None)
    client = Client()
    access_token = client.exchange_code_for_token(
        client_id=os.environ.get('STRAVA_CLIENT_ID', None),
        client_secret=os.environ.get('STRAVA_CLIENT_SECRET', None),
        code=code
    )
    request.session['access_token'] = access_token

    return redirect(index)


def logout(request):
    request.session.flush()
    return redirect(index)


def about(request):
    # TODO: handle logged in and not logged in users
    return render(request, 'about.html')


def profile(request):
    return render(request, 'profile.html')
