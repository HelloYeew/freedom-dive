from django.db import models
from martor.models import MartorField
from mdeditor.fields import MDTextField


class ScoreStore(models.Model):
    user_id = models.IntegerField()
    date = models.DateTimeField()
    beatmap_id = models.IntegerField()
    ruleset_short_name = models.CharField(max_length=100)
    passed = models.BooleanField(default=False)
    score_id = models.CharField(max_length=100)
    statistics = models.JSONField(default=dict)

    def __str__(self):
        return str(self.user_id) + ' - ' + self.date.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + self.ruleset_short_name


class PerformanceStore(models.Model):
    user_id = models.IntegerField()
    score_id = models.CharField(max_length=100)
    performance = models.JSONField(default=dict)

    def __str__(self):
        return str(self.user_id) + ' - ' + self.score_id


class PerformanceByGraphStore(models.Model):
    user_id = models.IntegerField()
    score_id = models.CharField(max_length=100)
    performance = models.JSONField(default=dict)

    def __str__(self):
        return str(self.user_id) + ' - ' + self.score_id


class ClientChangelog(models.Model):
    version = models.CharField(max_length=100)
    date = models.DateTimeField()
    public = models.BooleanField(default=False)
    content = MDTextField(null=True, blank=True)
    download_url_windows = models.URLField(max_length=300, null=True, blank=True)
    download_url_macos = models.URLField(max_length=300, null=True, blank=True)
    download_url_linux = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.version + ' - ' + self.date.strftime('%Y-%m-%d %H:%M:%S') + ' client changelog'


class WebChangelog(models.Model):
    version = models.CharField(max_length=100)
    date = models.DateTimeField()
    public = models.BooleanField(default=False)
    content = MDTextField(null=True, blank=True)

    def __str__(self):
        return self.version + ' - ' + self.date.strftime('%Y-%m-%d %H:%M:%S') + ' web changelog'
