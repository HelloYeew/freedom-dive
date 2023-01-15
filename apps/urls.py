from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('beatmapsets', views.beatmapset_list, name='beatmapset'),
    path('beatmapsets/<int:beatmapset_id>', views.beatmapset_detail, name='beatmapset_detail'),
    path('beatmapsets/<int:beatmapset_id>/beatmaps/<int:beatmap_id>', views.beatmap_detail, name='beatmap_detail'),
    path('scores', views.scores_list, name='scores'),
    path('scores/<int:score_id>', views.score_detail, name='score_detail'),
    path('changelog/client', views.client_changelog_list, name='client_changelog'),
    path('changelog/client/<str:version>', views.client_changelog_detail, name='client_changelog_detail'),
    path('changelog/web', views.web_changelog_list, name='web_changelog'),
    path('changelog/web/<str:version>', views.web_changelog_detail, name='web_changelog_detail'),
]