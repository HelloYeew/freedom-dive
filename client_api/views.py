import datetime
import json

from decouple import config
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import ScoreStore

CLIENT_ID = int(config('CLIENT_ID', default='10'))
CLIENT_SECRET = config('CLIENT_SECRET', default='')

class SubmitSoloScoreView(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
        # TODO: Ignore -1 ruleset ID and name
        if request.data['client_id'] == CLIENT_ID and request.data['client_secret'] == CLIENT_SECRET:
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
