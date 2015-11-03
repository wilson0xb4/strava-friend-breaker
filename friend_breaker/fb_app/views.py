from __future__ import unicode_literals
from __future__ import print_function
import os

from django.conf import settings
from django.shortcuts import render, redirect
from stravalib import Client

from models import Athlete, ChallengedSegment
from tasks import massive_test


def index(request):
    access_token = request.session.get('access_token', None)
    if access_token is None:
        # if access_token is NOT in session, kickoff the oauth exchange
        client = Client()
        url = client.authorization_url(
            client_id=os.environ.get('STRAVA_CLIENT_ID', None),
            redirect_uri=settings.ALLOWED_HOSTS[0] + '/authorization'
            # redirect_uri='http://127.0.0.1:8000/authorization'
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


def update(request):
    '''
    Kickoff the update process! (using celery)
    '''

    # check that I have both an `access_token` and an `athlete_id`
    # essentially, "is the user logged in"
    if not request.session.get('access_token', False) and request.session.get('athlete_id', False):
        # could redirect 401 or 403 instead...but just put them at the home page
        return redirect(index)

    # client = Client(access_token=request.session.get('access_token', None))
    access_token = request.session.get('access_token', None)
    athlete_id = request.session.get('athlete_id', None)

    # context = _build_context(client, athlete_id)
    massive_test.delay(access_token, athlete_id)

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
