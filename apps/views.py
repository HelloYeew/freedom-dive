import json

from django.core.paginator import Paginator
from django.shortcuts import render

from apps.models import ScoreStore
from mirror.models import BeatmapSet, Beatmap
from users.models import ColourSettings
from utility.osu_database import get_beatmapset_by_id, get_user_by_id, get_beatmap_by_id
from utility.utils import get_osu_beatmap_statistics


def homepage(request):
    latest_score = ScoreStore.objects.latest('id')
    try:
        beatmap = Beatmap.objects.get(beatmap_id=latest_score.beatmap_id)
        beatmapset = BeatmapSet.objects.get(beatmapset_id=beatmap.beatmapset.beatmapset_id)
    except BeatmapSet.DoesNotExist or Beatmap.DoesNotExist:
        beatmap = get_beatmap_by_id(latest_score.beatmap_id)
        beatmapset = beatmap.beatmapset
    except:
        beatmap = None
        beatmapset = None
    user = get_user_by_id(latest_score.user_id)
    latest_score = {
        'score': latest_score,
        'user': user,
        'beatmap': beatmap,
        'beatmapset': beatmapset,
        'score_json': latest_score.statistics
    }
    if request.user.is_authenticated:
        return render(request, 'homepage.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'latest_score': latest_score
        })
    else:
        return render(request, 'homepage.html', {
            'latest_score': latest_score
        })


def beatmapset_list(request):
    beatmaps = BeatmapSet.objects.all().order_by('-beatmapset_id')
    paginator = Paginator(beatmaps, 30)
    page_number = request.GET.get('page')
    beatmaps_pagination = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, 'apps/beatmaps/beatmaps.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'statistics_osu': get_osu_beatmap_statistics(),
            'beatmapsets': beatmaps_pagination
        })
    else:
        return render(request, 'apps/beatmaps/beatmaps.html', {
            'statistics_osu': get_osu_beatmap_statistics(),
            'beatmapsets': beatmaps_pagination
        })


def beatmapset_detail(request, beatmapset_id):
    beatmapset = BeatmapSet.objects.get(beatmapset_id=beatmapset_id)
    beatmaps = Beatmap.objects.filter(beatmapset=beatmapset).order_by('difficulty_rating')
    if request.user.is_authenticated:
        return render(request, 'apps/beatmaps/beatmaps_detail.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'beatmapset': beatmapset,
            'beatmaps': beatmaps
        })
    else:
        return render(request, 'apps/beatmaps/beatmaps_detail.html', {
            'beatmapset': beatmapset,
            'beatmaps': beatmaps
        })


def scores_list(request):
    score = ScoreStore.objects.all().order_by('-id')
    score_list = []
    for i in score:
        try:
            beatmap = Beatmap.objects.get(beatmap_id=i.beatmap_id)
            beatmapset = BeatmapSet.objects.get(beatmapset_id=beatmap.beatmapset.beatmapset_id)
        except BeatmapSet.DoesNotExist or Beatmap.DoesNotExist:
            beatmap = get_beatmap_by_id(i.beatmap_id)
            beatmapset = beatmap.beatmapset
        except:
            beatmap = None
            beatmapset = None
        user = get_user_by_id(i.user_id)
        score_list.append({
            'score': i,
            'user': user,
            'beatmap': beatmap,
            'beatmapset': beatmapset
        })
    if request.user.is_authenticated:
        return render(request, 'apps/scores/scores.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'scores': score_list
        })
    else:
        return render(request, 'apps/scores/scores.html', {
            'scores': score_list
        })


def score_detail(request, score_id):
    score = ScoreStore.objects.get(id=score_id)
    try:
        beatmap = Beatmap.objects.get(beatmap_id=score.beatmap_id)
        beatmapset = BeatmapSet.objects.get(beatmapset_id=beatmap.beatmapset.beatmapset_id)
    except BeatmapSet.DoesNotExist or Beatmap.DoesNotExist:
        beatmap = get_beatmap_by_id(score.beatmap_id)
        beatmapset = beatmap.beatmapset
    except:
        beatmap = None
        beatmapset = None
    user = get_user_by_id(score.user_id)
    score_json = json.dumps(score.statistics, indent=4)
    if request.user.is_authenticated:
        return render(request, 'apps/scores/scores_detail.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'score': score,
            'user': user,
            'beatmap': beatmap,
            'beatmapset': beatmapset,
            'score_json': score_json
        })
    else:
        return render(request, 'apps/scores/scores_detail.html', {
            'score': score,
            'user': user,
            'beatmap': beatmap,
            'beatmapset': beatmapset,
            'score_json': score_json
        })
