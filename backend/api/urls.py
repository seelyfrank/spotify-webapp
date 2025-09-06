from django.urls import path
from django.contrib.auth import views as auth_views
from . import spotify_views

urlpatterns = [
    path("auth/login/", auth_views.LoginView.as_view(), name="login"),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("spotify/login/", spotify_views.spotify_login, name="spotify_login"),
    path("spotify/callback/", spotify_views.spotify_callback, name="spotify_callback"),
    path("spotify/top-tracks/<str:time_range>/", spotify_views.get_top_tracks, name="top_tracks")
]