import json
import traceback

import sentry_sdk
from decouple import config
from django.core.paginator import Paginator
from django.shortcuts import render

from apps.models import ScoreStore, ClientChangelog, WebChangelog
from ayaka import settings
from mirror.models import BeatmapSet, Beatmap
from users.models import ColourSettings
from utility.osu_database import get_beatmapset_by_id, get_user_by_id, get_beatmap_by_id
from utility.ruleset.score_processor.utils import get_readable_score
from utility.utils import get_osu_beatmap_statistics

S3_URL = config('S3_URL', default='https://freedom-dive-assets.nyc3.digitaloceanspaces.com')


def homepage(request):
    latest_score = ScoreStore.objects.filter(passed=True).order_by('-id').first()
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
            'latest_score': latest_score,
            's3_url': S3_URL
        })
    else:
        return render(request, 'homepage.html', {
            'latest_score': latest_score,
            's3_url': S3_URL
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
            'beatmapsets': beatmaps_pagination,
            's3_url': S3_URL
        })
    else:
        return render(request, 'apps/beatmaps/beatmaps.html', {
            'statistics_osu': get_osu_beatmap_statistics(),
            'beatmapsets': beatmaps_pagination,
            's3_url': S3_URL
        })


def beatmapset_detail(request, beatmapset_id):
    try:
        beatmapset = BeatmapSet.objects.get(beatmapset_id=beatmapset_id)
    except BeatmapSet.DoesNotExist:
        # try to get beatmapset from main database
        beatmapset = get_beatmapset_by_id(beatmapset_id)
        if beatmapset is None:
            # return 404
            return render(request, '404.html', status=404)
    beatmaps = Beatmap.objects.filter(beatmapset=beatmapset).order_by('difficulty_rating')
    if request.user.is_authenticated:
        return render(request, 'apps/beatmaps/beatmaps_detail.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'beatmapset': beatmapset,
            'beatmaps': beatmaps,
            's3_url': S3_URL
        })
    else:
        return render(request, 'apps/beatmaps/beatmaps_detail.html', {
            'beatmapset': beatmapset,
            'beatmaps': beatmaps,
            's3_url': S3_URL
        })


def scores_list(request):
    score = ScoreStore.objects.filter(passed=True).order_by('-id')
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
    score_object = ScoreStore.objects.get(id=score_id)
    # We don't want to show the score if it's not passed
    if not score_object.passed:
        return render(request, '404.html', status=404)
    osu_user = get_user_by_id(score_object.user_id)
    try:
        beatmap = Beatmap.objects.get(beatmap_id=score_object.beatmap_id)
        beatmapset = BeatmapSet.objects.get(beatmapset_id=beatmap.beatmapset.beatmapset_id)
    except BeatmapSet.DoesNotExist or Beatmap.DoesNotExist:
        beatmap = get_beatmap_by_id(score_object.beatmap_id)
        beatmapset = beatmap.beatmapset
    except:
        beatmap = None
        beatmapset = None
    user = get_user_by_id(score_object.user_id)
    score_json = json.dumps(score_object.statistics, indent=4)
    rich_render = True
    try:
        score = get_readable_score(score_object)
    except Exception as e:
        if settings.DEBUG:
            traceback.print_exc()
        score = None
        rich_render = False
    if rich_render:
        if score['ruleset_id'] == 0:
            return render(request, 'apps/scores/scores_detail_osu.html', {
                'colour_settings': ColourSettings.objects.get(user=request.user) if request.user.is_authenticated else None,
                'osu_user': osu_user,
                'score_object': score_object,
                'score': score,
                'score_json': score_json,
                'score_user': user,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                's3_url': S3_URL
            })
        elif score['ruleset_id'] == 4:
            beatmap.play_mode = 4
            return render(request, 'apps/scores/scores_detail_tau.html', {
                'colour_settings': ColourSettings.objects.get(user=request.user) if request.user.is_authenticated else None,
                'osu_user': osu_user,
                'score_object': score_object,
                'score': score,
                'score_json': score_json,
                'score_user': user,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                's3_url': S3_URL
            })
        elif score['ruleset_id'] == 5:
            beatmap.play_mode = 5
            return render(request, 'apps/scores/scores_detail_sentakki.html', {
                'colour_settings': ColourSettings.objects.get(user=request.user) if request.user.is_authenticated else None,
                'osu_user': osu_user,
                'score_object': score_object,
                'score': score,
                'score_json': score_json,
                'score_user': user,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                's3_url': S3_URL
            })
        else:
            # This should not be reached but just put it as a fallback page
            return render(request, 'apps/scores/scores_detail_legacy.html', {
                'score_json': score_json,
                'score_user': user,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                's3_url': S3_URL
            })
    else:
        if request.user.is_authenticated:
            return render(request, 'apps/scores/scores_detail_legacy.html', {
                'colour_settings': ColourSettings.objects.get(user=request.user),
                'score_json': score_json,
                'score_user': user,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                's3_url': S3_URL
            })
        else:
            return render(request, 'apps/scores/scores_detail_legacy.html', {
                'score_json': score_json,
                'score_user': user,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                's3_url': S3_URL
            })


def client_changelog_list(request):
    changelog = ClientChangelog.objects.filter(public=True).order_by('-date')
    if request.user.is_authenticated:
        return render(request, 'apps/changelog/client_changelog_list.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'changelog': changelog
        })
    else:
        return render(request, 'apps/changelog/client_changelog_list.html', {
            'changelog': changelog
        })


def web_changelog_list(request):
    changelog = WebChangelog.objects.filter(public=True).order_by('-date')
    if request.user.is_authenticated:
        return render(request, 'apps/changelog/web_changelog_list.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'changelog': changelog
        })
    else:
        return render(request, 'apps/changelog/web_changelog_list.html', {
            'changelog': changelog
        })


def client_changelog_detail(request, version):
    try:
        changelog = ClientChangelog.objects.get(version=version)
    except ClientChangelog.DoesNotExist:
        return render(request, '404.html', status=404)
    if changelog.public is False and request.user.is_authenticated is False:
        return render(request, '404.html', status=404)
    if request.user.is_authenticated:
        return render(request, 'apps/changelog/client_changelog_detail.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'changelog': changelog
        })
    else:
        return render(request, 'apps/changelog/client_changelog_detail.html', {
            'changelog': changelog
        })


def web_changelog_detail(request, version):
    try:
        changelog = WebChangelog.objects.get(version=version)
    except WebChangelog.DoesNotExist:
        return render(request, '404.html', status=404)
    if changelog.public is False and request.user.is_authenticated is False:
        return render(request, '404.html', status=404)
    if request.user.is_authenticated:
        return render(request, 'apps/changelog/web_changelog_detail.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'changelog': changelog
        })
    else:
        return render(request, 'apps/changelog/web_changelog_detail.html', {
            'changelog': changelog
        })