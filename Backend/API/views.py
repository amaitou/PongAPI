
from .serializers import UserRegistrationSerializer, UserUpdateSerializer, GetUserBasicInfoSerializer, GetGameStatsSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from .authentication import CookieTokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from .models import UserInfo, UserGameStats
import time

class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        if request.data['password'] != request.data['re_password']:
            return Response({'error': 'Passwords do not match'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            return Response({"message": "User already logged in"}, status=status.HTTP_200_OK)

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({"message": "User logged in successfully"})
        response.set_cookie(settings.ACCESS_TOKEN, access_token, httponly=True)
        response.set_cookie(settings.REFRESH_TOKEN, refresh_token, httponly=True)

        return response

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = UserInfo.objects.get(username=request.user)
        game = UserGameStats.objects.get(user_id=user.id)
        
        user_basic_info = UserRegistrationSerializer(user)
        game_stats = GetGameStatsSerializer(game)

        serializers = [user_basic_info.data, game_stats.data]
        return Response(serializers, status=status.HTTP_200_OK)

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

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
    
class UpdateUser(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        access_token = request.COOKIES.get(settings.ACCESS_TOKEN)

        user = UserInfo.objects.get(username=request.user)
        serializer = UserUpdateSerializer(user, data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST) 
        
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        
        if request.user.username == username:
            return Response('redirect',
                            status=status.HTTP_302_FOUND,
                            headers={'Location': '/api/profile/'})

        try:
            user = UserInfo.objects.get(username=username)
        except UserInfo.DoesNotExist:
            return Response({'error': 'Player not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = GetUserBasicInfoSerializer(user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

class GetGameStats(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        game_stats = UserGameStats.objects.get(user_id=request.user.id)
        serializer = GetGameStatsSerializer(game_stats)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)