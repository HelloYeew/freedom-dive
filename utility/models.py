from django.contrib.auth.models import User
from django.db import models


class UtilityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    field = models.CharField(max_length=100)
    description = models.TextField(default='')
    status = models.IntegerField(default=0)  # 0 = pending, 1 = running, 2 = done, 3 = error

    def __str__(self):
        return f'{self.user} - {self.field} - {self.time}'


class ImportBeatmapsetUsageLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    beatmapset_id = models.IntegerField()
    success = models.BooleanField(default=False)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.beatmapset_id} - {self.time} - {self.success}'
