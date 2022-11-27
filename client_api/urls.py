from django.urls import path

from .views import SubmitSoloScoreView, ClientUserRegistration

urlpatterns = [
    path('score', SubmitSoloScoreView.as_view(), name='api_client_score_submission'),
    path('user/register', ClientUserRegistration.as_view(), name='api_client_user_registration')
]
