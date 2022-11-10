from django.db import models


class ScoreStore(models.Model):
    user_id = models.IntegerField()
    date = models.DateTimeField()
    beatmap_id = models.IntegerField()
    ruleset_short_name = models.CharField(max_length=100)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_id) + ' - ' + self.date.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + self.ruleset_short_name
