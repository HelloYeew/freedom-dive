from PIL import Image
from decouple import config
from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User

S3_URL = config('S3_URL', default='')


class ColourSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color_primary = ColorField(default='#DFD9D6')
    color_accent = ColorField(default='#F9F7B4')
    color_background = ColorField(default='#0A0A0A')
    mask_opacity = models.FloatField(default=0.7, max_length=1)

    def __str__(self):
        return self.user.username + '\'s colour settings'


class SiteSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    use_traditional_metadata = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + '\'s site settings'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar', default='avatar/default.png')
    avatar_s3_url = models.URLField(default=S3_URL + '/avatar/pfp.png')

    def __str__(self):
        return self.user.username + '\'s profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 256 or img.width > 256:
                output_size = (256, 256)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


class SignUpRequest(models.Model):
    username = models.CharField(max_length=255)
    osu_user_id = models.IntegerField(default=0)
    authentication_key = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.username + '\'s sign up request'


class OsuOauthTemporaryCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username + '\'s temporary code'


class OsuOauthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=1000)
    refresh_token = models.CharField(max_length=1000)
    expires_in = models.IntegerField(default=0)
    token_type = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '\'s oauth token'
