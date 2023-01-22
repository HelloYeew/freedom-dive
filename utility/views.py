import random
import string
import traceback

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from client_api.models import BeatmapsetImportAPIUsageLog, BeatmapConvertedStatisticsImportAPIUsageLog, \
    BeatmapsetLookupAPIUsageLog
from mirror.models import BeatmapSet
from mirror.utils import import_beatmapset_to_mirror, import_beatmap_to_mirror
from users.models import ColourSettings, SignUpRequest
from utility.forms import ImportSpecificBeatmapSetForm, CreateSignUpRequestForm
from utility.models import UtilityLog, ImportBeatmapsetUsageLog
from utility.osu_database import import_beatmapset_from_api, get_beatmapset_by_id, get_beatmap_by_beatmapset
from utility.utils import get_osu_beatmap_statistics, get_mirror_beatmap_statistics, download_beatmap_pic_to_s3


@login_required
def utility(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'utility/utility.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'statistics_osu': get_osu_beatmap_statistics(),
            'statistics_mirror': get_mirror_beatmap_statistics()
        })
    else:
        return render(request, '403.html', status=403)


@login_required
def utility_log(request):
    if request.user.is_superuser:
        return render(request, 'utility/utility_log.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'utility_log': UtilityLog.objects.all().order_by('-time')
        })
    else:
        return render(request, '403.html', status=403)


@login_required
def import_beatmapset_usage_log(request):
    if request.user.is_superuser:
        return render(request, 'utility/import_beatmapset_usage_log.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'import_beatmapset_usage_log': ImportBeatmapsetUsageLog.objects.all().order_by('-time'),
            'failed_count': ImportBeatmapsetUsageLog.objects.filter(success=False).count(),
        })
    else:
        return render(request, '403.html', status=403)


@login_required
def import_beatmapset_api_usage_log(request):
    if request.user.is_superuser:
        return render(request, 'utility/import_beatmapset_api_usage_log.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'import_beatmapset_usage_log': BeatmapsetImportAPIUsageLog.objects.all().order_by('-time'),
            'failed_count': BeatmapsetImportAPIUsageLog.objects.filter(success=False).count(),
        })
    else:
        return render(request, '403.html', status=403)


@login_required
def import_specific_beatmapset_from_osu_api(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            form = ImportSpecificBeatmapSetForm(request.POST)
            if form.is_valid():
                try:
                    import_beatmapset_from_api(form.cleaned_data['beatmapset_id'])
                    import_beatmapset_to_mirror(get_beatmapset_by_id(form.cleaned_data['beatmapset_id']))
                    beatmapset = get_beatmap_by_beatmapset(form.cleaned_data['beatmapset_id'])
                    download_beatmap_pic_to_s3(form.cleaned_data['beatmapset_id'])
                    for beatmap in beatmapset:
                        import_beatmap_to_mirror(beatmap)
                    messages.success(request, 'Imported beatmapset successfully!')
                    UtilityLog.objects.create(
                        user=request.user,
                        field='import_specific_beatmapset_from_osu_api',
                        status=2,
                        description=f'Imported beatmapset {form.cleaned_data["beatmapset_id"]} from osu! api'
                    )
                    return redirect('utility_log')
                except Exception as e:
                    messages.error(request, f'Importing beatmapset failed: ({e.__class__.__name__}) {e}')
                    if settings.DEBUG:
                        traceback.print_exc()
                    UtilityLog.objects.create(
                        user=request.user,
                        field='import_specific_beatmapset_from_osu_api',
                        status=3,
                        description=f'Importing beatmapset {form.cleaned_data["beatmapset_id"]} failed: ({e.__class__.__name__}) {e}'
                    )
                    return redirect('utility_log')
        else:
            form = ImportSpecificBeatmapSetForm()
        return render(request, 'utility/import_specific_beatmapset_from_osu_api.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'form': form
        })
    else:
        return render(request, '403.html', status=403)


@login_required()
def create_sign_up_request(request):
    if request.user.is_superuser or request.user.is_staff:
        colour_settings = ColourSettings.objects.filter(user=request.user).first()
        if request.method == 'POST':
            form = CreateSignUpRequestForm(request.POST)
            if form.is_valid():
                form.save()
                # get the object that was just created
                sign_up_request = SignUpRequest.objects.filter(username=form.cleaned_data['username']).first()
                # create random character and number for authentication key
                random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
                sign_up_request.authentication_key = random_string
                sign_up_request.save()
                UtilityLog.objects.create(
                    user=request.user,
                    field='create_sign_up_request',
                    status=2,
                    description=f'Created sign up request for {form.cleaned_data["username"]}'
                )
                url = request.build_absolute_uri('/')[:-1]
                messages.success(request, f'Sign up request created successfully! The request URL is {url}/signup?id={sign_up_request.id}&auth_key={sign_up_request.authentication_key}')
                return redirect('utility')
        else:
            form = CreateSignUpRequestForm()
        return render(request, 'utility/create_sign_up_request.html', {
            'colour_settings': colour_settings,
            'form': form
        })
    else:
        return render(request, '403.html', status=403)


@login_required
def import_beatmap_converted_statistics_usage_log(request):
    if request.user.is_superuser:
        return render(request, 'utility/import_beatmap_converted_statistics_usage_log.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'import_usage_log': BeatmapConvertedStatisticsImportAPIUsageLog.objects.all().order_by('-time')[:200],
            'failed_log': BeatmapConvertedStatisticsImportAPIUsageLog.objects.filter(success=False).order_by('-time')[:200],
            'failed_count': BeatmapConvertedStatisticsImportAPIUsageLog.objects.filter(success=False).count(),
        })
    else:
        return render(request, '403.html', status=403)


@login_required
def beatmapset_lookup_api_usage_log(request):
    if request.user.is_superuser:
        return render(request, 'utility/beatmapset_lookup_api_usage_log.html', {
            'colour_settings': ColourSettings.objects.get(user=request.user),
            'import_usage_log': BeatmapsetLookupAPIUsageLog.objects.all().order_by('-time')[:200],
            'failed_log': BeatmapsetLookupAPIUsageLog.objects.filter(success=False).order_by('-time')[:200],
            'failed_count': BeatmapsetLookupAPIUsageLog.objects.filter(success=False).count(),
        })
    else:
        return render(request, '403.html', status=403)
