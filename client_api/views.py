import json
import traceback

from decouple import config
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import ScoreStore
from mirror.models import BeatmapSet
from mirror.utils import import_beatmapset_to_mirror, import_beatmap_to_mirror
from utility.models import ImportBeatmapsetUsageLog
from utility.osu_database import get_beatmapset_by_id, import_beatmapset_from_api, get_beatmap_by_beatmapset
from utility.utils import download_beatmap_pic_to_s3

CLIENT_ID = int(config('CLIENT_ID', default='10'))
CLIENT_SECRET = config('CLIENT_SECRET', default='')

class SubmitSoloScoreView(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        # TODO: Ignore -1 ruleset ID and name
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            try:
                ScoreStore.objects.create(
                    user_id=request.data['user_id'],
                    # use timezone.now() if not passed for failed score
                    date=request.data['date'] if request.data['passed'] else timezone.now(),
                    beatmap_id=request.data['beatmap_id'],
                    ruleset_short_name=request.data['ruleset_short_name'],
                    passed=request.data['passed'],
                    # convert statistics from string to dict
                    statistics=json.loads(request.data['statistics'])
                )
            except Exception as e:
                print('ScoreStore not created : ' + str(e))
            return Response(status=status.HTTP_200_OK, data={'message': 'success'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})


class ClientUserRegistration(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            if request.data['username'] and request.data['email'] and request.data['password']:
                try:
                    user = User.objects.create_user(username=request.data['username'], email=request.data['email'],
                                                    password=request.data['password'])
                    user.save()
                    return Response(status=status.HTTP_200_OK, data={'message': 'success'})
                except Exception as e:
                    print('User not created : ' + str(e))
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'user creation failed'})
            else:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'missing parameters'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})


class ImportBeatmapsetRequest(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            if request.data['beatmapset_id']:
                try:
                    beatmapset_id = int(request.data['beatmapset_id'])
                    beatmaps = get_beatmapset_by_id(beatmapset_id)
                    if beatmaps:
                        download_beatmap_pic_to_s3(beatmapset_id)
                        ImportBeatmapsetUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=True,
                            description=f'Beatmapset {beatmaps.title} is already in the database'
                        )
                        return Response(status=status.HTTP_202_ACCEPTED, data={'message': f'Beatmapset {beatmaps.title} is already in the database!'})
                    try:
                        import_beatmapset_from_api(beatmapset_id)
                        import_beatmapset_to_mirror(get_beatmapset_by_id(beatmapset_id))
                        beatmapset = get_beatmap_by_beatmapset(beatmapset_id)
                        download_beatmap_pic_to_s3(beatmapset_id)
                        beatmaps = get_beatmapset_by_id(beatmapset_id)
                        for beatmap in beatmapset:
                            import_beatmap_to_mirror(beatmap)
                        ImportBeatmapsetUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=True,
                            description=f'Import beatmapset {beatmaps.title} successfully'
                        )
                        return Response(status=status.HTTP_200_OK, data={'message': f'Imported {BeatmapSet.objects.get(beatmapset_id=beatmapset_id).title} successfully!'})
                    except Exception as e:
                        if settings.DEBUG:
                            traceback.print_exc()
                        ImportBeatmapsetUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=False,
                            description=f'Importing beatmapset failed: ({e.__class__.__name__}) {e}'
                        )
                        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': 'Something went wrong while importing beatmapset :( We have been notified of this issue!'})
                except Exception as e:
                    if settings.DEBUG:
                        traceback.print_exc()
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': 'Something went wrong while importing beatmapset :( We have been notified of this issue!'})
            else:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'missing parameters'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})