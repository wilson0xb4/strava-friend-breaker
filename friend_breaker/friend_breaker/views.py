import os
from django.shortcuts import render, redirect
from stravalib import Client


def index_view(request):
    access_token = request.session.get('access_token', None)
    if access_token is None:
        # if access_token is NOT in session, kickoff the oauth exchange
        client = Client()
        url = client.authorization_url(
            client_id=os.environ.get('STRAVA_CLIENT_ID', None),
            redirect_uri='http://127.0.0.1:8000/authorization'
        )
        context = {'auth_url': url, 'access_token': access_token}
        return render(request, 'index.html', context)

    # otherwise, load authorized user
    athlete = request.session.get('athlete', None)
    if athlete is None:
        # if athlete is NOT already set, get athlete (attempting to reduce calls to the API)
        client = Client(access_token=access_token)
        athlete = client.get_athlete()
        request.session['athlete_id'] = athlete.id
        request.session['firstname'] = athlete.firstname

    return render(request, 'index_loggedin.html')


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

    return redirect(index_view)


def logout(request):
    request.session.flush()
    return redirect(index_view)


def about(request):
    return render(request, 'about.html')


def profile(request):
    return render(request, 'profile.html')
