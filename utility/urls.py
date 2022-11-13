from django.urls import path
from . import views

urlpatterns = [
    path('utility', views.utility, name='utility'),
    path('utility/log', views.utility_log, name='utility_log'),
    path('utility/import_beatmapset_from_osu_api', views.import_specific_beatmapset_from_osu_api, name='import_specific_beatmapset_from_osu_api')
]