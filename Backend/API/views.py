
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import PlayerInfoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import time
from .models import PlayerInfo

class RegisterView(APIView):
    def post(self, request):

        if request.data['password'] != request.data['re_password']:
            return Response({'error': 'Passwords do not match'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = PlayerInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        try:
            user = PlayerInfo.objects.get(username=request.data['username'])
        except PlayerInfo.DoesNotExist:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(request.data['password']):
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken.for_user(user)
        response = Response()

        response.set_cookie('access', str(token.access_token), httponly=True)
        response.set_cookie('refresh', str(token), httponly=True)
        response.status_code = status.HTTP_200_OK
        response.data = {
            'message': "Login successful"
        }
        return response

class GetPlayer(APIView):
    class TokenExpired(Exception):
        pass

    def get(self, request):
        access_token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get('refresh')

        if not access_token or not refresh_token:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            access_token = AccessToken(access_token)
        except InvalidToken:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            expiration = access_token['exp']
            if expiration < time.time():
                raise self.TokenExpired
        except self.TokenExpired:
            return Response({'error': 'Token was expired'}, status=status.HTTP_401_UNAUTHORIZED)

        player = PlayerInfo.objects.get(username=access_token['user_id'])
        serializer = PlayerInfoSerializer(player)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        refresh = request.COOKIES.get('refresh')
        if not refresh:
            return Response({'error': 'No refresh token provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except TokenError:
            return Response({'error': 'Invalid token or error blacklisting token.'},status=status.HTTP_400_BAD_REQUEST)

        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response