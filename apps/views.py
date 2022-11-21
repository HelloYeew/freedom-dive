from django.shortcuts import render

from users.models import ColourSettings
from utility.utils import get_osu_beatmap_statistics


def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'homepage.html', {'colour_settings': ColourSettings.objects.get(user=request.user)})
    else:
        return render(request, 'homepage.html')


def beatmaps(request):
    if request.user.is_authenticated:
        return render(request, 'apps/beatmaps/beatmaps.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'statistics_osu': get_osu_beatmap_statistics(),
        })
    else:
        return render(request, 'apps/beatmaps/beatmaps.html', {
            'statistics_osu': get_osu_beatmap_statistics(),
        })
