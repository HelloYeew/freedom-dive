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

from client_api.models import BeatmapsetImportAPIUsageLog, BeatmapConvertedStatisticsImportAPIUsageLog, \
    BeatmapsetLookupAPIUsageLog, BeatmapLookupAPIUsageLog
from mirror.models import BeatmapSet, ConvertedBeatmapInfo, ScoreStore, Performance, PerformanceByGraph
from mirror.utils import import_beatmapset_to_mirror, import_beatmap_to_mirror
from utility.osu_api import get_beatmap_object_from_api, get_beatmapset_object_from_api
from utility.osu_database import get_beatmapset_by_id, import_beatmapset_from_api, get_beatmap_by_beatmapset, \
    update_beatmapset_from_api, get_beatmap_by_id
from utility.ruleset.utils import get_ruleset_short_name
from utility.utils import download_beatmap_pic_to_s3

CLIENT_ID = int(config('CLIENT_ID', default='10'))
CLIENT_SECRET = config('CLIENT_SECRET', default='')


class DummyJsonView(APIView):
    """
    This view is for testing purposes. It just print the request data get from request and return success.
    """
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        print(request.data)
        return Response(status=status.HTTP_200_OK, data={'message': 'success'})

    def get(self, request):
        return Response(status=status.HTTP_200_OK, data={'message': 'success'})


class SubmitSoloScoreView(APIView):
    """
    API path for sending the score to server.
    This path require the client ID and secret authentication.
    """
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        # TODO: Ignore -1 ruleset ID and name
        # Note : On freedom-dive-server changed ruleset checking policy to not hacking since 2022-01-29
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            try:
                statistics = json.loads(request.data['statistics'])
                if statistics['ruleset_id'] == -1:
                    return Response(status=status.HTTP_200_OK, data={'message': 'success'})
                ScoreStore.objects.create(
                    user_id=request.data['user_id'],
                    # use timezone.now() if not passed for failed score
                    created_at=request.data['date'] if request.data['passed'] else timezone.now(),
                    updated_at=request.data['date'] if request.data['passed'] else timezone.now(),
                    beatmap_id=request.data['beatmap_id'],
                    ruleset_short_name=request.data['ruleset_short_name'],
                    passed=request.data['passed'],
                    # convert statistics from string to dict
                    data=json.loads(request.data['statistics']),
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
    """
    API path for sending username and password for registration on this database.
    This path will use when user register the account on the client to make it sync on both side.
    This path require the client ID and secret authentication.
    """
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
    """
    API path for request for importing the beatmap to the database.
    To make this path not be used on outside the client this path require the client ID and secret authentication.
    """
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            if request.data['beatmapset_id'] and request.data['beatmapset_id'] > 0:
                try:
                    beatmapset_id = int(request.data['beatmapset_id'])
                    beatmaps = get_beatmapset_by_id(beatmapset_id)
                    if beatmaps:
                        update_beatmapset_from_api(beatmapset_id)
                        # Since import_beatmapset_to_mirror() will update the existing beatmapset, so we can use this
                        import_beatmapset_to_mirror(get_beatmapset_by_id(beatmapset_id))
                        beatmapset = get_beatmap_by_beatmapset(beatmapset_id)
                        download_beatmap_pic_to_s3(beatmapset_id)
                        for beatmap in beatmapset:
                            import_beatmap_to_mirror(beatmap)
                        BeatmapsetImportAPIUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=True,
                            description=f'Beatmapset {beatmaps.title} is already in the database and updated.'
                        )
                        return Response(status=status.HTTP_202_ACCEPTED,
                                        data={'message': f'Beatmapset {beatmaps.title} has already been imported, '
                                                         f'and has been updated!'})
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


class BeatmapsLookupRequest(APIView):
    """
    API for using in client's GetBeatmapRequest (beatmaps/lookup) that don't need beatmap information update like ImportBeatmapsetRequest
    To make this path not be used on outside the client this path require the client ID and secret authentication.
    """
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            if request.data['beatmapset_id'] and request.data['beatmapset_id'] > 0:
                try:
                    beatmapset_id = int(request.data['beatmapset_id'])
                    beatmaps = get_beatmapset_by_id(beatmapset_id)
                    if beatmaps:
                        BeatmapLookupAPIUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=True,
                            description=f'Beatmapset {beatmaps.title} is already in the database, skipping import.'
                        )
                        return Response(status=status.HTTP_202_ACCEPTED,
                                        data={'message': f'Beatmapset {beatmaps.title} has already been imported!'})
                    else:
                        import_beatmapset_from_api(beatmapset_id)
                        import_beatmapset_to_mirror(get_beatmapset_by_id(beatmapset_id))
                        beatmapset = get_beatmap_by_beatmapset(beatmapset_id)
                        download_beatmap_pic_to_s3(beatmapset_id)
                        beatmaps = get_beatmapset_by_id(beatmapset_id)
                        for beatmap in beatmapset:
                            import_beatmap_to_mirror(beatmap)
                        BeatmapLookupAPIUsageLog.objects.create(
                            beatmapset_id=beatmapset_id,
                            success=True,
                            description=f'Import beatmapset {beatmaps.title} successfully'
                        )
                        return Response(status=status.HTTP_200_OK, data={
                            'message': f'Imported {BeatmapSet.objects.get(beatmapset_id=beatmapset_id).title} successfully! Now you can play it!'})
                except Exception as e:
                    if settings.DEBUG:
                        traceback.print_exc()
                    BeatmapLookupAPIUsageLog.objects.create(
                        beatmapset_id=request.data['beatmapset_id'],
                        success=False,
                        description=f'Importing beatmapset failed: ({e.__class__.__name__}) {e}'
                    )
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


class BeatmapsetsLookupRequest(APIView):
    """
    API for using in client's GetBeatmapsetRequest (beatmapsets/lookup) that don't need beatmap information update like
    ImportBeatmapsetRequest.
    This path is different from BeatmapsLookupRequest since in the osu! API beatmapset lookup path can add querystring
    `beatmap_id` to get the beatmapset information of the beatmap.
    To make this path not be used on outside the client this path require the client ID and secret authentication.
    Note : lookup_type can be either "set_id" or "beatmap_id"
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            if request.data['lookup_type'] and request.data['id'] > 0:
                if request.data['lookup_type'] == "beatmap_id":
                    beatmap = get_beatmap_by_id(int(request.data['id']))
                    if beatmap:
                        BeatmapsetLookupAPIUsageLog.objects.create(
                            lookup_type=request.data['lookup_type'],
                            lookup_id=request.data['id'],
                            success=True,
                            description=f'Beatmap {beatmap.version} ({beatmap.beatmapset_id}) is already in the database, skipping import.'
                        )
                        return Response(status=status.HTTP_202_ACCEPTED,
                                        data={'message': f'Beatmap {beatmap.version} ({beatmap.beatmapset_id}) has already been imported!'})
                    else:
                        beatmap_from_api = get_beatmap_object_from_api(int(request.data['id']))
                        if beatmap_from_api:
                            beatmapset_id = beatmap_from_api.beatmapset_id
                            import_beatmapset_from_api(beatmapset_id)
                            import_beatmapset_to_mirror(get_beatmapset_by_id(beatmapset_id))
                            beatmapset = get_beatmap_by_beatmapset(beatmapset_id)
                            download_beatmap_pic_to_s3(beatmapset_id)
                            beatmaps = get_beatmapset_by_id(beatmapset_id)
                            for beatmap in beatmapset:
                                import_beatmap_to_mirror(beatmap)
                            BeatmapsetLookupAPIUsageLog.objects.create(
                                lookup_type=request.data['lookup_type'],
                                lookup_id=request.data['id'],
                                success=True,
                                description=f'Import beatmapset {beatmaps.title} successfully'
                            )
                            return Response(status=status.HTTP_200_OK, data={
                                'message': f'Imported {BeatmapSet.objects.get(beatmapset_id=beatmapset_id).title} successfully! Now you can play it!'})
                        else:
                            BeatmapsetLookupAPIUsageLog.objects.create(
                                lookup_type=request.data['lookup_type'],
                                lookup_id=request.data['id'],
                                success=False,
                                description=f'Beatmap {request.data["id"]} not found in the osu! API'
                            )
                            return Response(status=status.HTTP_404_NOT_FOUND,
                                            data={'message': f'Beatmap {request.data["id"]} not found in the osu! API'})
                elif request.data['lookup_type'] == "set_id":
                    beatmapset = get_beatmapset_by_id(int(request.data['id']))
                    if beatmapset:
                        BeatmapsetLookupAPIUsageLog.objects.create(
                            lookup_type=request.data['lookup_type'],
                            lookup_id=request.data['id'],
                            success=True,
                            description=f'Beatmapset {beatmapset.title} is already in the database, skipping import.'
                        )
                        return Response(status=status.HTTP_202_ACCEPTED,
                                        data={'message': f'Beatmapset {beatmapset.title} has already been imported!'})
                    else:
                        beatmapset_from_api = get_beatmapset_object_from_api(int(request.data['id']))
                        if beatmapset_from_api:
                            import_beatmapset_from_api(int(request.data['id']))
                            import_beatmapset_to_mirror(get_beatmapset_by_id(int(request.data['id'])))
                            beatmapset = get_beatmap_by_beatmapset(int(request.data['id']))
                            download_beatmap_pic_to_s3(int(request.data['id']))
                            for beatmap in beatmapset:
                                import_beatmap_to_mirror(beatmap)
                            BeatmapsetLookupAPIUsageLog.objects.create(
                                lookup_type=request.data['lookup_type'],
                                lookup_id=request.data['id'],
                                success=True,
                                description=f'Import beatmapset {beatmapset_from_api.title} successfully'
                            )
                            return Response(status=status.HTTP_200_OK, data={
                                'message': f'Imported {BeatmapSet.objects.get(beatmapset_id=int(request.data["id"])).title} successfully! Now you can play it!'})
                        else:
                            BeatmapsetLookupAPIUsageLog.objects.create(
                                lookup_type=request.data['lookup_type'],
                                lookup_id=request.data['id'],
                                success=False,
                                description=f'Beatmapset {request.data["id"]} not found in the osu! API'
                            )
                            return Response(status=status.HTTP_404_NOT_FOUND,
                                            data={'message': f'Beatmapset {request.data["id"]} not found in the osu! API'})
                else:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'invalid lookup type'})
            else:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'message': 'missing parameters'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'client unauthorized'})


class ImportBeatmapConvertedStatistics(APIView):
    """
    API path for importing the converted beatmap statistics to the database.
    This path require the client ID and secret authentication.
    """
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
    """
    API path for submitting performance data to the database.
    This path require the client ID and secret authentication.
    """
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            try:
                Performance.objects.create(
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
    """
    API path for submitting performance data to the database via graph component from client.
    This path require the client ID and secret authentication.
    """
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        if int(request.data['client_id']) == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
            try:
                PerformanceByGraph.objects.create(
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