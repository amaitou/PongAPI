
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from .authentication import CookieTokenAuthentication
from .serializers import PlayerRegistrationSerializer, PlayerUpdateSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from .models import PlayerInfo
import time

class RegisterView(APIView):

    authentication_classes = [CookieTokenAuthentication]

    def post(self, request):

        if request.data['password'] != request.data['re_password']:
            return Response({'error': 'Passwords do not match'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PlayerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):

    authentication_classes = [CookieTokenAuthentication]

    def post(self, request):
        if request.user.is_authenticated:
            return Response({"message": "User already logged in"}, status=200)

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({"message": "User logged in successfully"})
            response.set_cookie(settings.ACCESS_TOKEN, access_token, httponly=True)
            response.set_cookie(settings.REFRESH_TOKEN, refresh_token, httponly=True)
            return response
        else:
            return Response({"error": "Invalid credentials"}, status=400)

class GetPlayer(APIView):

    authentication_classes = [CookieTokenAuthentication]

    def get(self, request):

        if not request.user.is_authenticated:
            return Response({'error': 'User not logged in.'},
                            status=status.HTTP_400_BAD_REQUEST)

        access_token = request.COOKIES.get(settings.ACCESS_TOKEN)

        if not access_token:
            return Response({'error': 'No token provided.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            access_token = AccessToken(access_token)
        except TokenError:
            return Response({'error': 'Invalid token.'},
                            status=InvalidToken.status_code)
        
        try:
            player = PlayerInfo.objects.get(id=access_token['user_id'])
        except PlayerInfo.DoesNotExist:
            return Response({'error': 'Player not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = PlayerRegistrationSerializer(player)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

class LogoutView(APIView):

    authentication_classes = [CookieTokenAuthentication]

    def post(self, request):

        if not request.user.is_authenticated:
            return Response({'error': 'User not logged in.'},
                            status=status.HTTP_400_BAD_REQUEST)

        refresh = request.COOKIES.get(settings.REFRESH_TOKEN)
        if not refresh:
            return Response({'error': 'No refresh token provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except TokenError:
            return Response({'error': 'Invalid token or error blacklisting token.'},status=status.HTTP_400_BAD_REQUEST)

        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.ACCESS_TOKEN)
        response.delete_cookie(settings.REFRESH_TOKEN)
        return response
    
class UpdatePlayer(APIView):

    authentication_classes = [CookieTokenAuthentication]

    def put(self, request):
        access_token = request.COOKIES.get(settings.ACCESS_TOKEN)

        if not access_token:
            return Response({'error': 'No token provided.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            access_token = AccessToken(access_token)
        except TokenError:
            return Response({'error': 'Invalid token.'},
                            status=InvalidToken.status_code)

        player = PlayerInfo.objects.get(id=access_token['user_id'])
        serializer = PlayerUpdateSerializer(player, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST) 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)