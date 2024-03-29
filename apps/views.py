import json
import traceback

from decouple import config
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from apps.models import ClientChangelog, WebChangelog, PerformanceStore
from ayaka import settings
from mirror.models import BeatmapSet, Beatmap, ConvertedBeatmapInfo, ScoreStore, Performance
from users.models import ColourSettings, SiteSettings
from utility.osu_database import get_beatmapset_by_id, get_user_by_id, get_beatmap_by_id
from utility.ruleset.score_processor.utils import get_readable_score
from utility.ruleset.utils import get_ruleset_id
from utility.utils import get_osu_beatmap_statistics

S3_URL = config('S3_URL', default='https://freedom-dive-assets.nyc3.digitaloceanspaces.com')


def homepage(request):
    """
    View for site's homepage
    """
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
        'score_json': latest_score.data
    }
    if request.user.is_authenticated:
        return render(request, 'homepage.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'latest_score': latest_score,
            's3_url': S3_URL,
            'site_settings': SiteSettings.objects.get(user=request.user)
        })
    else:
        return render(request, 'homepage.html', {
            'latest_score': latest_score,
            's3_url': S3_URL
        })


def beatmapset_list(request):
    """
    View for beatmaps list page
    """
    beatmaps = BeatmapSet.objects.all().order_by('-beatmapset_id')
    paginator = Paginator(beatmaps, 30)
    page_number = request.GET.get('page')
    beatmaps_pagination = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, 'apps/beatmaps/beatmaps.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'statistics_osu': get_osu_beatmap_statistics(),
            'beatmapsets': beatmaps_pagination,
            's3_url': S3_URL,
            'site_settings': SiteSettings.objects.get(user=request.user)
        })
    else:
        return render(request, 'apps/beatmaps/beatmaps.html', {
            'statistics_osu': get_osu_beatmap_statistics(),
            'beatmapsets': beatmaps_pagination,
            's3_url': S3_URL
        })


def beatmapset_detail(request, beatmapset_id):
    """
    View for beatmapset detail.
    TODO: Make it more support osu! path
    """
    try:
        beatmapset = BeatmapSet.objects.get(beatmapset_id=beatmapset_id)
    except BeatmapSet.DoesNotExist:
        # try to get beatmapset from the main database
        beatmapset = get_beatmapset_by_id(beatmapset_id)
        if beatmapset is None:
            # return 404
            return render(request, '404.html', status=404)
    beatmaps = Beatmap.objects.filter(beatmapset=beatmapset).order_by('difficulty_rating')
    if request.user.is_authenticated:
        return render(request, 'apps/beatmaps/beatmapset_detail.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'beatmapset': beatmapset,
            'beatmaps': beatmaps,
            's3_url': S3_URL,
            'site_settings': SiteSettings.objects.get(user=request.user)
        })
    else:
        return render(request, 'apps/beatmaps/beatmapset_detail.html', {
            'beatmapset': beatmapset,
            'beatmaps': beatmaps,
            's3_url': S3_URL
        })


def beatmap_detail(request, beatmapset_id, beatmap_id):
    try:
        beatmap = Beatmap.objects.get(beatmap_id=beatmap_id)
        beatmapset = BeatmapSet.objects.get(beatmapset_id=beatmapset_id)
    except BeatmapSet.DoesNotExist:
        # Return 404
        return render(request, '404.html', status=404)
    except Beatmap.DoesNotExist:
        # Redirect to beatmapset detail
        return redirect('beatmapset_detail', beatmapset_id=beatmapset_id)
    # Check if the beatmap is in the beatmapset
    if beatmap.beatmapset != beatmapset:
        # redirect to beatmapset detail page
        return redirect('beatmapset_detail', beatmapset_id=beatmapset_id)
    # Remove converted info that has ruleset ID equal to beatmap's ruleset ID
    # Also exclude if ruleset_id is -1 for safety
    converted_beatmap_info = ConvertedBeatmapInfo.objects.filter(beatmap_id=beatmap_id).exclude(ruleset_id=beatmap.play_mode).exclude(ruleset_id=-1).order_by('ruleset_id')
    # Get only passed scores
    all_score = ScoreStore.objects.filter(beatmap_id=beatmap_id).order_by('-created_at').exclude(passed=False)
    # Create a new list that contain only unique ruleset_short_name in all_score
    ruleset_per_score = {}
    for score in all_score:
        # Check that ruleset is in key of ruleset_per_score
        if score.ruleset_short_name not in ruleset_per_score:
            ruleset_per_score[score.ruleset_short_name] = []
        # Append score to the list
        ruleset_per_score[score.ruleset_short_name].append(score)
    ruleset_list = list(ruleset_per_score.keys())
    # Sort ruleset_list by get ruleset ID using get_ruleset_id function and sort it
    ruleset_id = []
    for ruleset in ruleset_list:
        ruleset_id.append({
            "id": get_ruleset_id(ruleset),
            "name": ruleset
        })
    ruleset_id = sorted(ruleset_id, key=lambda k: k['id'])
    # Get only the name of ruleset back to ruleset_list for convenience
    ruleset_list = []
    for ruleset in ruleset_id:
        ruleset_list.append(ruleset['name'])
    if request.user.is_authenticated:
        return render(request, 'apps/beatmaps/beatmaps_detail.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'beatmapset': beatmapset,
            'beatmap': beatmap,
            's3_url': S3_URL,
            'converted_beatmap_info': converted_beatmap_info,
            'site_settings': SiteSettings.objects.get(user=request.user),
            'score_rulesets': ruleset_list,
            'ruleset_per_score': ruleset_per_score
        })
    else:
        return render(request, 'apps/beatmaps/beatmaps_detail.html', {
            'beatmapset': beatmapset,
            'beatmap': beatmap,
            's3_url': S3_URL,
            'converted_beatmap_info': converted_beatmap_info,
            'score_rulesets': ruleset_list,
            'ruleset_per_score': ruleset_per_score
        })


def scores_list(request):
    """
    View for score list page. This page is temporary since we don't show any score on any page.
    This page must be removed when we can show score on other place.
    """
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
            'scores': score_list,
            'site_settings': SiteSettings.objects.get(user=request.user)
        })
    else:
        return render(request, 'apps/scores/scores.html', {
            'scores': score_list
        })


def score_detail(request, score_id):
    """
    View for showing score detail get from score ID as parameter.
    """
    score_object = ScoreStore.objects.get(id=score_id)
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
    failed = not score_object.passed
    score_json = json.dumps(score_object.data, indent=4)
    # Check that this score can use a new score page or not
    rich_render = True
    try:
        score = get_readable_score(score_object)
    except Exception as e:
        if settings.DEBUG:
            traceback.print_exc()
        score = None
        rich_render = False
    # Extract PP from performance database
    if Performance.objects.filter(score_id=score_object.score_id, user_id=score_object.user_id).exists():
        try:
            performance = Performance.objects.get(score_id=score_object.score_id, user_id=score_object.user_id).performance
            pp = int(round(performance['pp']))
            # Calculate rich details of performance
            # Get all key of performance detail
            performance_detail_keys = list(performance.keys())
            performance_detail = []
            for key in performance_detail_keys:
                performance_detail.append({
                    'key': key,
                    'value': performance[key],
                    'percent': performance[key] / performance["pp"] * 100
                })
        except:
            if settings.DEBUG:
                traceback.print_exc()
            pp = 0
            performance = None
            performance_detail = None
    else:
        pp = 0
        performance = None
        performance_detail = None
    if rich_render:
        if score['ruleset_id'] == 0:
            return render(request, 'apps/scores/scores_detail_osu.html', {
                'colour_settings': ColourSettings.objects.get(user=request.user) if request.user.is_authenticated else None,
                'osu_user': osu_user,
                'score_object': score_object,
                'score': score,
                'score_json': score_json,
                'score_user': user,
                'failed': failed,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                'pp': pp,
                'performance': performance,
                'performance_detail': performance_detail,
                's3_url': S3_URL,
                'site_settings': SiteSettings.objects.get(user=request.user) if request.user.is_authenticated else None
            })
        elif score['ruleset_id'] == 1004:
            beatmap.play_mode = 1004
            return render(request, 'apps/scores/scores_detail_tau.html', {
                'colour_settings': ColourSettings.objects.get(user=request.user) if request.user.is_authenticated else None,
                'osu_user': osu_user,
                'score_object': score_object,
                'score': score,
                'score_json': score_json,
                'score_user': user,
                'failed': failed,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                'pp': pp,
                'performance': performance,
                'performance_detail': performance_detail,
                's3_url': S3_URL,
                'site_settings': SiteSettings.objects.get(user=request.user) if request.user.is_authenticated else None
            })
        elif score['ruleset_id'] == 1005:
            beatmap.play_mode = 1005
            return render(request, 'apps/scores/scores_detail_sentakki.html', {
                'colour_settings': ColourSettings.objects.get(user=request.user) if request.user.is_authenticated else None,
                'osu_user': osu_user,
                'score_object': score_object,
                'score': score,
                'score_json': score_json,
                'score_user': user,
                'failed': failed,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                'pp': pp,
                'performance': performance,
                'performance_detail': performance_detail,
                's3_url': S3_URL,
                'site_settings': SiteSettings.objects.get(user=request.user) if request.user.is_authenticated else None
            })
        else:
            # This should not be reached but just put it as a fallback page
            return render(request, 'apps/scores/scores_detail_legacy.html', {
                'colour_settings': ColourSettings.objects.get(user=request.user) if request.user.is_authenticated else None,
                'score_json': score_json,
                'score_user': user,
                'failed': failed,
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
                'failed': failed,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                's3_url': S3_URL,
                'site_settings': SiteSettings.objects.get(user=request.user)
            })
        else:
            return render(request, 'apps/scores/scores_detail_legacy.html', {
                'score_json': score_json,
                'score_user': user,
                'failed': failed,
                'beatmap': beatmap,
                'beatmapset': beatmapset,
                's3_url': S3_URL
            })


def client_changelog_list(request):
    """
    View for client changelog list
    """
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
    """
    View for web changelog list.
    """
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
    """
    View for client changelog detail from version in parameter.
    """
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
    """
    View for web changelog detail from version in parameter.
    """
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