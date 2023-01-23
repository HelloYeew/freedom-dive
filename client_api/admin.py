from django.contrib import admin

from client_api.models import BeatmapsetImportAPIUsageLog, BeatmapsetLookupAPIUsageLog, BeatmapLookupAPIUsageLog, \
    BeatmapConvertedStatisticsImportAPIUsageLog

# Register your models here.
admin.site.register(BeatmapsetImportAPIUsageLog)
admin.site.register(BeatmapsetLookupAPIUsageLog)
admin.site.register(BeatmapLookupAPIUsageLog)
admin.site.register(BeatmapConvertedStatisticsImportAPIUsageLog)