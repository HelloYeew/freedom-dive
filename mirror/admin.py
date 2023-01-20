from django.contrib import admin
from .models import *

admin.site.register(Beatmap)
admin.site.register(BeatmapSet)
admin.site.register(Score)
admin.site.register(ScoreStore)
admin.site.register(Performance)
admin.site.register(PerformanceByGraph)
admin.site.register(ConvertedBeatmapInfo)
