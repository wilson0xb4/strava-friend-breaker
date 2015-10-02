import os
from django.shortcuts import render, redirect
from stravalib import Client


def index_view(request):
    access_token = request.session.get('access_token', 'None')
    if access_token is not None:
        client = Client(access_token=access_token)
        athlete = client.get_athlete()
        context = {'athlete': athlete}
        return render(request, 'index_loggedin.html', context)

    client = Client()
    url = client.authorization_url(
        client_id=os.environ.get('STRAVA_CLIENT_ID', None),
        redirect_uri='http://127.0.0.1:8000/authorization'
    )
    context = {'auth_url': url, 'access_token': access_token}
    return render(request, 'index.html', context)


def authorization_view(request):
    '''
    Trades in the `code` sent from Strava for an `access_token`.
    Ties that `access_token` to a users session.
    '''

    code = request.GET.get('code', None)
    client = Client()
    access_token = client.exchange_code_for_token(
        client_id=os.environ.get('STRAVA_CLIENT_ID', None),
        client_secret=os.environ.get('STRAVA_CLIENT_SECRET', None),
        code=code)

    request.session['access_token'] = access_token

    return redirect(index_view)
