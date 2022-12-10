from django.db import models

class BeatmapsetImportAPIUsageLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    beatmapset_id = models.IntegerField()
    success = models.BooleanField(default=False)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.beatmapset_id} - {self.time} - {self.success}'