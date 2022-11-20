from django.urls import path
from . import views

urlpatterns = [
    path('utility', views.utility, name='utility'),
    path('utility/log/import-beatmapset-usage', views.import_beatmapset_usage_log, name='import_beatmapset_usage_log'),
    path('utility/log', views.utility_log, name='utility_log'),
    path('utility/import_beatmapset_from_osu_api', views.import_specific_beatmapset_from_osu_api, name='import_specific_beatmapset_from_osu_api'),
    path('beatmaps/import', views.import_beatmaps_from_osu_public, name='import_beatmaps_from_osu_public')
]