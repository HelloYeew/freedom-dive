from django.db import models


class BeatmapsetImportAPIUsageLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    beatmapset_id = models.IntegerField()
    success = models.BooleanField(default=False)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.beatmapset_id} - {self.time} - {self.success}'


class BeatmapsetLookupAPIUsageLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    lookup_type = models.CharField(max_length=100, default='')
    lookup_id = models.IntegerField()
    success = models.BooleanField(default=False)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.lookup_type} - {self.lookup_id} - {self.time} - {self.success}'


class BeatmapLookupAPIUsageLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    beatmapset_id = models.IntegerField()
    success = models.BooleanField(default=False)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.beatmapset_id} - {self.time} - {self.success}'


class BeatmapConvertedStatisticsImportAPIUsageLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    beatmap_id = models.IntegerField()
    success = models.BooleanField(default=False)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.beatmap_id} - {self.time} - {self.success}'
