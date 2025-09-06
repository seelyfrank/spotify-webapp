import os, requests, datetime
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import UserSpotifyData
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE = "user-library-read user-read-recently-played user-top-read"

@login_required
def spotify_login(request):
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return redirect(url)

@login_required
def spotify_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    r = requests.post("https://accounts.spotify.com/api/token", data=payload)
    data = r.json()

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    expires_in = data["expires_in"]

    usd, _ = UserSpotifyData.objects.get_or_create(user=request.user)
    usd.access_token = access_token
    usd.refresh_token = refresh_token
    usd.token_expires = timezone.now() + datetime.timedelta(seconds=expires_in)
    usd.save()

    return redirect("/dashboard/")  

def refresh_spotify_token(user):
    usd = UserSpotifyData.objects.get(user=user)
    if usd.token_expires > timezone.now():
        return usd.access_token

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": usd.refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    r = requests.post("https://accounts.spotify.com/api/token", data=payload)
    data = r.json()
    usd.access_token = data["access_token"]
    usd.token_expires = timezone.now() + datetime.timedelta(seconds=data["expires_in"])
    usd.save()
    return usd.access_token

@login_required
def get_top_tracks(request, time_range="medium_term"):
    access_token = refresh_spotify_token(request.user)
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"time_range": time_range, "limit": 50}
    r = requests.get("https://api.spotify.com/v1/me/top/tracks", headers=headers, params=params)
    return JsonResponse(r.json())