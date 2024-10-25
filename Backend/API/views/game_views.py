
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.game_serializer import GameResultRecordingSerializer
from rest_framework import status
from ..models import UserInfo
from rest_framework.serializers import ValidationError


class GameResultRecordingView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:

        try:
            player_1 = UserInfo.objects.get(username = request.data['winner'])
            player_2 = UserInfo.objects.get(username = request.data['loser'])
        except UserInfo.DoesNotExist:
            return Response({
                'message': 'One or more players do not exist'
            }, status = status.HTTP_400_BAD_REQUEST)

        data = {
            'player_1': player_1.pk,
            'player_2': player_2.pk,
            'score_1': request.data['winner_score'],
            'score_2': request.data['loser_score'],
        }
        serializer = GameResultRecordingSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
                'error': e.detail
            },
            status = status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({
            'message': 'Game result was recorded successfully'
        }, status = status.HTTP_200_OK)
        