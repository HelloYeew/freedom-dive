import datetime
import json

from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import ScoreStore
from mirror.models import Score


# Create a dummy django rest framework view that will print the request body to the console
class SubmitSoloScoreView(APIView):
    permissions_classes = [permissions.AllowAny]

    def post(self, request):
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
