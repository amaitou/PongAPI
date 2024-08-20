
from .serializers import    UserRegistrationSerializer, UserUpdateSerializer, \
							GetUserBasicInfoSerializer, GetGameStatsSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .models import UserInfo, UserGameStats
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import requests
from .jwt import create_token_for_user

class RegisterView(APIView):

	permission_classes = [AllowAny]

	def __check_password(self, password: str, re_password: str) -> bool:

		if not password and not re_password:
			return True
		return password == re_password

	def post(self, request) -> Response:

		if not self.__check_password(request.data.get('password'), request.data.get('re_password')):
			return Response({
				'message': 'Passwords do not match',
				'redirect': False,
				'redirect_url': ''
			}, status=status.HTTP_400_BAD_REQUEST)

		serializer = UserRegistrationSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response ({
				'message': 'User registered successfully',
				'redirect': True,
				'redirect_url': '/api/login/',
				'data': serializer.data,
				'jwt': create_token_for_user(serializer.instance)
			}, status=status.HTTP_201_CREATED)
		else:
			return Response({
				'message': 'Invalid data',
				'redirect': False,
				'redirect_url': ''
			}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

	permission_classes = [AllowAny]

	def post(self, request):
		if request.user.is_authenticated:
			return Response({
				'message': 'User already logged in',
				'status': status.HTTP_200_OK,
				'redirect': True,
				'redirect_url': '/api/profile/'
			})

		username = request.data.get("username")
		password = request.data.get("password")
		user = authenticate(request, username=username, password=password)

		if not user:
			return Response({
				'message': 'Invalid credentials',
				'status': status.HTTP_401_UNAUTHORIZED,
				'redirect': False,
				'redirect_url': ''
			})
		
		tokens = create_token_for_user(user)
		access_token = tokens['access_token']
		refresh_token = tokens['refresh_token']

		response = Response({
			'message': 'Login successful',
			'redirect': True,
			'redirect_url': '/api/profile'
		}, status=status.HTTP_200_OK)

		response.set_cookie(settings.ACCESS_TOKEN, access_token)
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

class Authentication42(APIView):

	permission_classes = [AllowAny]

	def get(self, request):
		
		code = request.GET.get('code')
		if not code:
			return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
		
		data = {
			'grant_type': 'authorization_code',
			'client_id': settings.CLIENT_ID,
			'client_secret': settings.CLIENT_SECRET,
			'code': code.encode('utf-8'),
			'redirect_uri': settings.REDIRECT,
		}

		__token = requests.post("https://api.intra.42.fr/oauth/token/", data=data)

		if not "access_token" in __token.json():
			return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
		
		access_token = __token.json()['access_token']

		user = requests.get("https://api.intra.42.fr/v2/me", headers={
			'Authorization': f'Bearer {access_token}'
		})

		user = user.json()

		first_name = user['first_name']
		last_name = user['last_name']
		username = user['login']
		email = user['email']

		serializer = UserRegistrationSerializer(data={
			'username': username,
			'first_name': first_name,
			'last_name': last_name,
			'email': email
		})

		if serializer.is_valid():
			serializer.save()
			return Response({
				'message': 'User registered successfully',
				'redirect': True,
				'redirect_url': '/api/login/',
				'data': serializer.data,
				'jwt': create_token_for_user(serializer.instance)
			}, status=status.HTTP_201_CREATED)
		else:
			return Response({
				'message': 'Invalid data',
				'redirect': False,
				'redirect_url': ''
			}, status=status.HTTP_400_BAD_REQUEST)