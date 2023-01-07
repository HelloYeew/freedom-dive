from django.urls import path

from .views import *

urlpatterns = [
    # path('dummy', DummyJsonView.as_view(), name='api_client_dummy'),
    path('score', SubmitSoloScoreView.as_view(), name='api_client_score_submission'),
    path('performance', PerformanceSubmission.as_view(), name='api_client_performance_submission'),
    path('performance/graph', PerformanceSubmissionByGraph.as_view(), name='api_client_performance_submission_by_graph'),
    path('user/register', ClientUserRegistration.as_view(), name='api_client_user_registration'),
    path('beatmapset/import', ImportBeatmapsetRequest.as_view(), name='api_client_import_beatmapset_request'),
    path('beatmaps/statistics', ImportBeatmapConvertedStatistics.as_view(), name='api_client_import_beatmapset_converted_statistics')
]
