import json
import traceback

import sentry_sdk
from decouple import config
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import ScoreStore, PerformanceStore, PerformanceByGraphStore
from client_api.models import BeatmapsetImportAPIUsageLog, BeatmapConvertedStatisticsImportAPIUsageLog
from mirror.models import BeatmapSet, ConvertedBeatmapInfo
from mirror.utils import import_beatmapset_to_mirror, import_beatmap_to_mirror
from utility.osu_database import get_beatmapset_by_id, import_beatmapset_from_api, get_beatmap_by_beatmapset
from utility.ruleset.utils import get_ruleset_short_name
from utility.utils import download_beatmap_pic_to_s3

CLIENT_ID = int(config('CLIENT_ID', default='10'))
CLIENT_SECRET = config('CLIENT_SECRET', default='')


class DummyJsonView(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        print(request.data)
        return Response(status=status.HTTP_200_OK, data={'message': 'success'})

    def get(self, request):
        return Response(status=status.HTTP_200_OK, data={'message': 'success'})


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
                    statistics=json.loads(request.data['statistics']),
                    score_id=request.data['score_id']
                )
            except Exception as e:
                sentry_sdk.set_context("payload", request.data)
                sentry_sdk.capture_exception(e)
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
                    sentry_sdk.set_context("payload", request.data)
                    sentry_sdk.capture_exception(e)
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'user creation failed'})
            else:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'missing parameters'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})


class ImportBeatmapsetRequest(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            if request.data['beatmapset_id'] and request.data['beatmapset_id'] > 0:
                try:
                    beatmapset_id = int(request.data['beatmapset_id'])
                    beatmaps = get_beatmapset_by_id(beatmapset_id)
                    if beatmaps:
                        download_beatmap_pic_to_s3(beatmapset_id)
                        BeatmapsetImportAPIUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=True,
                            description=f'Beatmapset {beatmaps.title} is already in the database'
                        )
                        return Response(status=status.HTTP_202_ACCEPTED,
                                        data={'message': f'Beatmapset {beatmaps.title} has already been imported!'})
                    try:
                        import_beatmapset_from_api(beatmapset_id)
                        import_beatmapset_to_mirror(get_beatmapset_by_id(beatmapset_id))
                        beatmapset = get_beatmap_by_beatmapset(beatmapset_id)
                        download_beatmap_pic_to_s3(beatmapset_id)
                        beatmaps = get_beatmapset_by_id(beatmapset_id)
                        for beatmap in beatmapset:
                            import_beatmap_to_mirror(beatmap)
                        BeatmapsetImportAPIUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=True,
                            description=f'Import beatmapset {beatmaps.title} successfully'
                        )
                        return Response(status=status.HTTP_200_OK, data={
                            'message': f'Imported {BeatmapSet.objects.get(beatmapset_id=beatmapset_id).title} successfully! Now you can play it!'})
                    except Exception as e:
                        if settings.DEBUG:
                            traceback.print_exc()
                        BeatmapsetImportAPIUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=False,
                            description=f'Importing beatmapset failed: ({e.__class__.__name__}) {e}'
                        )
                        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
                            'message': 'Something went wrong while importing beatmapset :( We have been notified of this issue!'})
                except Exception as e:
                    if settings.DEBUG:
                        traceback.print_exc()
                    sentry_sdk.set_context("payload", request.data)
                    sentry_sdk.capture_exception(e)
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
                        'message': 'Something went wrong while importing beatmapset :( We have been notified of this issue!'})
            else:
                if request.data['beatmapset_id'] <= 0:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    data={'message': 'Invalid beatmapset ID'})
                else:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'missing parameters'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})


class ImportBeatmapConvertedStatistics(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            if request.data['beatmap_id'] and request.data['beatmap_id'] > 0 and request.data['ruleset_id'] > -1:
                beatmap_id = int(request.data['beatmap_id'])
                ruleset_id = int(request.data['ruleset_id'])
                try:
                    beatmap_statistics = request.data
                    # remove ruleset_id, beatmap_id, client_id, client_secret from beatmap_statistics
                    del beatmap_statistics['ruleset_id']
                    del beatmap_statistics['beatmap_id']
                    del beatmap_statistics['client_id']
                    del beatmap_statistics['client_secret']
                    if ConvertedBeatmapInfo.objects.filter(beatmap_id=beatmap_id, ruleset_id=ruleset_id).exists():
                        ConvertedBeatmapInfo.objects.filter(beatmap_id=beatmap_id, ruleset_id=ruleset_id).update(
                            statistics=beatmap_statistics
                        )
                        BeatmapConvertedStatisticsImportAPIUsageLog.objects.create(
                            beatmap_id=beatmap_id,
                            success=True,
                            description=f'Update beatmap statistics for beatmap {beatmap_id} with ruleset {get_ruleset_short_name(ruleset_id)} successfully'
                        )
                    else:
                        ConvertedBeatmapInfo.objects.create(
                            beatmap_id=beatmap_id,
                            ruleset_id=ruleset_id,
                            statistics=beatmap_statistics
                        )
                        BeatmapConvertedStatisticsImportAPIUsageLog.objects.create(
                            beatmap_id=beatmap_id,
                            success=True,
                            description=f'Import beatmap statistics for beatmap {beatmap_id} with ruleset {get_ruleset_short_name(ruleset_id)} successfully'
                        )
                    return Response(status=status.HTTP_200_OK, data={'message': 'success'})
                except Exception as e:
                    if settings.DEBUG:
                        traceback.print_exc()
                    BeatmapConvertedStatisticsImportAPIUsageLog.objects.create(
                        beatmap_id=beatmap_id,
                        success=False,
                        description=f'Import beatmap statistics failed: ({e.__class__.__name__}) {e}'
                    )
                    sentry_sdk.set_context("payload", request.data)
                    sentry_sdk.capture_exception(e)
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
                        'message': 'Something went wrong while importing beatmap statistics :( We have been notified of this issue!'})
            else:
                if request.data['beatmap_id'] <= 0:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'Invalid beatmap ID'})
                elif request.data['ruleset_id'] <= -1:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'Invalid ruleset ID'})
                else:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'missing parameters'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})


class PerformanceSubmission(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            try:
                PerformanceStore.objects.create(
                    user_id=request.data['user_id'],
                    score_id=request.data['score_id'],
                    performance=request.data['pp']
                )
                return Response(status=status.HTTP_200_OK, data={'message': 'success'})
            except Exception as e:
                if settings.DEBUG:
                    traceback.print_exc()
                sentry_sdk.set_context("payload", request.data)
                sentry_sdk.capture_exception(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
                    'message': 'Something went wrong while importing performance :( We have been notified of this issue!'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})


class PerformanceSubmissionByGraph(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            try:
                PerformanceByGraphStore.objects.create(
                    user_id=request.data['user_id'],
                    score_id=request.data['score_id'],
                    performance=request.data['pp']
                )
                return Response(status=status.HTTP_200_OK, data={'message': 'success'})
            except Exception as e:
                if settings.DEBUG:
                    traceback.print_exc()
                sentry_sdk.set_context("payload", request.data)
                sentry_sdk.capture_exception(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
                    'message': 'Something went wrong while importing performance :( We have been notified of this issue!'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})