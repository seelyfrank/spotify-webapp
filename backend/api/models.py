from django.db import models
from django.contrib.auth.models import User

class UserSpotifyData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    token_expires = models.DateTimeField()

    
