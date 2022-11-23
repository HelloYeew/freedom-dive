from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('beatmaps', views.beatmaps_list, name='beatmaps'),
    path('scores', views.scores_list, name='scores'),
    path('scores/<int:score_id>', views.score_detail, name='score_detail'),
]