from django.urls import path

from .views import SubmitSoloScoreView

urlpatterns = [
    path('score', SubmitSoloScoreView.as_view(), name='score'),
]
