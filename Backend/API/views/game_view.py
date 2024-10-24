
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

class RecordGameResultsView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        
        user = request.user
        data = request.data