from django.urls import path

from .views import *

urlpatterns = [
    # path('dummy', DummyJsonView.as_view(), name='api_client_dummy'),
    path('score', SubmitSoloScoreView.as_view(), name='api_client_score_submission'),
    path('user/register', ClientUserRegistration.as_view(), name='api_client_user_registration'),
    path('beatmapset/import', ImportBeatmapsetRequest.as_view(), name='api_client_import_beatmapset_request'),
    path('beatmaps/statistics', ImportBeatmapConvertedStatistics.as_view(), name='api_client_import_beatmapset_converted_statistics')
]
