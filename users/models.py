from decouple import config
from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User

S3_URL = config('S3_URL', default='https://freedom-dive-assets.nyc3.digitaloceanspaces.com')


class ColourSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color_primary = ColorField(default='#DFD9D6')
    color_accent = ColorField(default='#DBC2D1')
    color_background = ColorField(default='#0A0A0A')
    mask_opacity = models.FloatField(default=0.7, max_length=1)

    def __str__(self):
        return self.user.username + '\'s colour settings'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField(default=S3_URL + '/pfp.png')

    def __str__(self):
        return self.user.username + '\'s profile'


class SignUpRequest(models.Model):
    username = models.CharField(max_length=255)
    osu_user_id = models.IntegerField(default=0)
    authentication_key = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.username + '\'s sign up request'