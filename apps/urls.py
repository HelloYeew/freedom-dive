from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('beatmaps', views.beatmaps, name='beatmaps'),
]