from django.db import models
from django.utils import timezone

from utility.ruleset.utils import get_ruleset_short_name


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


class Score(models.Model):
    """
    Database table for storing the score sent from client.
    """
    score_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    beatmap_id = models.IntegerField()
    ruleset_id = models.IntegerField()
    data = models.JSONField()
    has_replay = models.BooleanField(default=False)
    preserve = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return str(self.score_id) + ' by ' + str(self.user_id)


class ConvertedBeatmapInfo(models.Model):
    beatmap_id = models.IntegerField()
    ruleset_id = models.IntegerField()
    statistics = models.JSONField()

    def __str__(self):
        return str(self.beatmap_id) + ' in ' + str(get_ruleset_short_name(self.ruleset_id))
