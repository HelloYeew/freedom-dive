from django.db import models
from django.utils import timezone

from utility.ruleset.utils import get_ruleset_short_name, get_ruleset_name


class BeatmapSet(models.Model):
    """
    Database table to store the beatmapset detail. This database is for showing in website purpose.
    For real beatmapset detail it lives in osu! MySQL database.
    For more information see BeatmapSet object structure in utility/database_models.py
    """
    beatmapset_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    artist = models.CharField(max_length=255)
    artist_unicode = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    title_unicode = models.CharField(max_length=255, blank=True, null=True)
    creator = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    tags = models.CharField(max_length=1000)
    video = models.BooleanField(default=False)
    storyboard = models.BooleanField(default=False)
    epilepsy = models.BooleanField(default=False)
    bpm = models.FloatField(default=0)
    approved = models.IntegerField(default=0)
    approved_date = models.DateTimeField(default=None, null=True)
    submit_date = models.DateTimeField(default=None, null=True)
    last_update = models.DateTimeField(default=None, null=True)
    display_title = models.CharField(max_length=255)
    genre_id = models.IntegerField(default=0)
    language_id = models.IntegerField(default=0)
    download_disabled = models.BooleanField(default=False)
    favorite_count = models.IntegerField(default=0)
    play_count = models.IntegerField(default=0)
    difficulty_names = models.CharField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return self.artist + ' - ' + self.title + ' [' + self.creator + ']'


class Beatmap(models.Model):
    """
    Database table to store the beatmap detail. This database is for showing in website purpose.
    For real beatmap detail it lives in osu! MySQL database.
    For more information see Beatmap object structure in utility/database_models.py
    """
    beatmap_id = models.IntegerField(primary_key=True)
    beatmapset = models.ForeignKey(BeatmapSet, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    filename = models.CharField(max_length=255)
    checksum = models.CharField(max_length=32)
    version = models.CharField(max_length=255)
    total_length = models.IntegerField(default=0)
    hit_length = models.IntegerField(default=0)
    count_total = models.IntegerField(default=0)
    count_normal = models.IntegerField(default=0)
    count_slider = models.IntegerField(default=0)
    count_spinner = models.IntegerField(default=0)
    diff_drain = models.FloatField(default=0)
    diff_size = models.FloatField(default=0)
    diff_overall = models.FloatField(default=0)
    diff_approach = models.FloatField(default=0)
    play_mode = models.IntegerField(default=0)
    approved = models.IntegerField(default=0)
    last_update = models.DateTimeField(default=timezone.now, null=True)
    difficulty_rating = models.FloatField(default=0)
    play_count = models.IntegerField(default=0)
    pass_count = models.IntegerField(default=0)
    bpm = models.FloatField(default=0)

    def __str__(self):
        return self.beatmapset.artist + ' - ' + self.beatmapset.title + ' [' + self.version + ']'

class ScoreStore(models.Model):
    """
    Database table for storing score sent from client
    Migrated from old ScoreStore in apps/models.py
    - 2023-01-20 : Change `statistics` field name to `data`
    """
    score_id = models.CharField(max_length=100)
    user_id = models.IntegerField()
    beatmap_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)
    ruleset_short_name = models.CharField(max_length=100)
    passed = models.BooleanField(default=False)
    data = models.JSONField(default=dict)
    client_version = models.CharField(max_length=100, blank=True, null=True)
    client_md5 = models.CharField(max_length=100, blank=True, null=True)
    client_platform = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user_id) + ' - ' + str(self.beatmap_id) + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + self.ruleset_short_name


class Performance(models.Model):
    """
    Database table for storing performance data
    Migrated from old PerformanceStore in apps/models.py
    """
    user_id = models.IntegerField()
    score_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    performance = models.JSONField(default=dict)

    def __str__(self):
        return str(self.user_id) + ' - ' + self.score_id


class PerformanceByGraph(models.Model):
    """
    Database table for storing performance data
    Migrated from old PerformanceStore in apps/models.py
    """
    user_id = models.IntegerField()
    score_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    performance = models.JSONField(default=dict)

    def __str__(self):
        return str(self.user_id) + ' - ' + self.score_id


class ConvertedBeatmapInfo(models.Model):
    beatmap_id = models.IntegerField()
    ruleset_id = models.IntegerField()
    statistics = models.JSONField()

    def __str__(self):
        return str(self.beatmap_id) + ' in ' + str(get_ruleset_short_name(self.ruleset_id))


class Country(models.Model):
    acronym = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255)
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CountryStatistics(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    ruleset_id = models.IntegerField()
    ranked_score = models.BigIntegerField(default=0)
    play_count = models.BigIntegerField(default=0)
    user_count = models.BigIntegerField(default=0)
    pp = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.country.acronym) + ' in ' + str(get_ruleset_name(self.ruleset_id))
