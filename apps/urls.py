from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('beatmapsets', views.beatmapset_list, name='beatmapset'),
    path('beatmapsets/<int:beatmapset_id>', views.beatmapset_detail, name='beatmapset_detail'),
    path('scores', views.scores_list, name='scores'),
    path('scores/<int:score_id>', views.score_detail, name='score_detail'),
]