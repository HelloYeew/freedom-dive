import traceback

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from mirror.utils import import_beatmapset_to_mirror, import_beatmap_to_mirror
from users.models import ColourSettings
from utility.forms import ImportSpecificBeatmapSetForm
from utility.models import UtilityLog
from utility.osu_database import import_beatmapset_from_api, get_beatmapset_by_id, get_beatmap_by_beatmapset


@login_required
def utility(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'utility/utility.html', {'colour_settings': ColourSettings.objects.get(user=request.user)})
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
def import_specific_beatmapset_from_osu_api(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            form = ImportSpecificBeatmapSetForm(request.POST)
            if form.is_valid():
                try:
                    import_beatmapset_from_api(form.cleaned_data['beatmapset_id'])
                    import_beatmapset_to_mirror(get_beatmapset_by_id(form.cleaned_data['beatmapset_id']))
                    beatmapset = get_beatmap_by_beatmapset(form.cleaned_data['beatmapset_id'])
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