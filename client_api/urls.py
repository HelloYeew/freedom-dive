from django.urls import path

from .views import SubmitSoloScoreView, ClientUserRegistration

urlpatterns = [
    path('score', SubmitSoloScoreView.as_view(), name='score'),
    path('user/register', ClientUserRegistration.as_view(), name='user_client_register')
]
