
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from ..serializers.user_serializer import RegistrationSerializer
from ..models import UserInfo
from ..utils import Utils
from rest_framework import serializers
import requests

class RegisterView(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def post(self, request: Request) -> Response:

		serializer = RegistrationSerializer(data=request.data)

		try:
			serializer.is_valid(raise_exception=True)
		except serializers.ValidationError as e:
			return Response({
				'error': e.detail,
				'redirect': True,
				'redirect_url': '/api/register/'
			},
			status=status.HTTP_400_BAD_REQUEST)

		serializer.save()

		# tokens = Utils.create_jwt_for_user(serializer.instance)

		# current_site = get_current_site(request).domain
		# relative_link = reverse('email_verification')
		# absurl = f'http://{current_site}{relative_link}?token={str(tokens["refresh_token"])}'
		# email_body = f'Hi {serializer.instance.username},\n\nPlease use the link below to verify your email address:\n{absurl}'
		# data = {
		# 	'domain': absurl,
		# 	'subject': 'Verify your email',
		# 	'email': serializer.instance.email,
		# 	'body': email_body
		# }

		# Utils.send_verification_email(data)

		return Response ({
			'success': 'User registered successfully, check your email for verification',
			'redirect': True,
			'redirect_url': '/api/login/',
			'output': serializer.data,
		},
		status=status.HTTP_201_CREATED)

class Authentication42View(APIView):

	permission_classes = [AllowAny]

	def __init__(self):
		self.code = ""
		self.data = {
			'grant_type': 'authorization_code',
			'client_id': settings.CLIENT_ID,
			'client_secret': settings.CLIENT_SECRET,
			'code': self.code.encode('utf-8'),
			'redirect_uri': settings.REDIRECT,
		}

	def __get_code(self, request: Request) -> str:
		self.code = request.GET.get('code')
		return self.code
	
	def __get_token(self) -> str:
		__token = requests.post("https://api.intra.42.fr/oauth/token/", data=self.data)
		if not "access_token" in __token.json():
			return None
		return __token.json()['access_token']

	def __get_user(self, access_token: str) -> dict:
		user = requests.get("https://api.intra.42.fr/v2/me", headers={
			'Authorization': f'Bearer {access_token}'
		})
		return user.json()
	
	def __set_code_in_data(self, code: str) -> None:
		self.data['code'] = code.encode('utf-8')

	def __register_user(self, user: dict) -> None:

		first_name = user['first_name']
		last_name = user['last_name']
		username = user['login']
		email = user['email']
		avatar = user['image']['link']

		serializer = RegistrationSerializer(data={
			'username': username,
			'first_name': first_name,
			'last_name': last_name,
			'email': email
		})

		if serializer.is_valid():
			serializer.save()

			response = Response({
				'success': 'User registered successfully',
				'redirect': True,
				'redirect_url': '/api/profile/',
				'output': serializer.data,
			},
			status=status.HTTP_201_CREATED)

			__jwt = Utils.create_jwt_for_user(serializer.instance)

			response.set_cookie(settings.ACCESS_TOKEN, __jwt['access_token'], httponly=False)
			response.set_cookie(settings.REFRESH_TOKEN, __jwt['refresh_token'], httponly=True)

			return response

		else:
			try:
				user = UserInfo.objects.get(username=username)
			except UserInfo.DoesNotExist:
				return Response({
					'error': 'failed to authenticate',
					'redirect': True,
					'redirect_url': '/api/login/'
				},
				status=status.HTTP_400_BAD_REQUEST)
			
			response = Response({
				'success': 'Login successful',
				'redirect': True,
				'redirect_url': '/api/profile',
			},
			status=status.HTTP_200_OK)

			__jwt = Utils.create_jwt_for_user(user)

			response.set_cookie(settings.ACCESS_TOKEN, __jwt['access_token'], httponly=False)
			response.set_cookie(settings.REFRESH_TOKEN, __jwt['refresh_token'], httponly=True)

			return response

	def get(self, request: Request) -> Response:

		if request.user.is_authenticated:
			return Response({
				'success': 'User already logged in',
				'redirect': True,
				'redirect_url': '/api/profile/'
			},
			status=status.HTTP_200_OK)
		
		self.code = self.__get_code(request)
		self.__set_code_in_data(self.code)

		if not self.code:
			return Response({
				'error': 'No code was provided',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		access_token = self.__get_token()

		if not access_token:
			return Response({
				'error': 'Failed to authenticate',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_400_BAD_REQUEST)

		user = self.__get_user(access_token)
		return self.__register_user(user)

class LoginView(APIView):

	permission_classes = [AllowAny]

	def post(self, request: Request) -> Response:
		if request.user.is_authenticated:
			return Response({
				'success': 'User already logged in',
				'redirect': True,
				'redirect_url': '/api/profile/'
			},
			status=status.HTTP_200_OK)

		username = request.data.get("username")
		password = request.data.get("password")

		user = authenticate(request, username=username, password=password)

		if not user:
			return Response({
				'error': 'Invalid username or password',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_401_UNAUTHORIZED)
		
		# if not user.is_verified:
		# 	return Response({
		# 		'error': 'User is not verified, check your email',
		# 		'redirect': True,
		# 		'redirect_url': '/api/login/',
		# 	},
		# 	status=status.HTTP_401_UNAUTHORIZED)

		response = Response({
			'success': 'Login successful',
			'redirect': True,
			'redirect_url': '/api/profile'
		},
		status=status.HTTP_200_OK)

		__jwt = Utils.create_jwt_for_user(user)

		response.set_cookie(settings.ACCESS_TOKEN, __jwt[settings.ACCESS_TOKEN], httponly=False)
		response.set_cookie(settings.REFRESH_TOKEN, __jwt[settings.REFRESH_TOKEN], httponly=True)

		return response

class LogoutView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:

		refresh = request.COOKIES.get(settings.REFRESH_TOKEN)

		if not refresh:
			return Response({
				'error': 'No refresh token was provided',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_400_BAD_REQUEST)

		try:
			token = RefreshToken(refresh)
			token.blacklist()
		except TokenError:
			return Response({
				'error': 'Refresh token is invalid, expired or blacklisted',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_401_UNAUTHORIZED)

		response = Response({
			'success': 'Logout successful',
			'redirect': True,
			'redirect_url': '/api/login/'
		},
		status=status.HTTP_200_OK)

		response.delete_cookie(settings.ACCESS_TOKEN)
		response.delete_cookie(settings.REFRESH_TOKEN)

		return response

class EmailVerifyView(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def get(self, request: Request) -> Response:

		token = request.GET.get('token')

		if not token:
			return Response({
				'error': 'No token provided',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			token = RefreshToken(token)
		except TokenError:
			return Response({
				'error': 'Refresh token is invalid, expired or blacklisted',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_401_UNAUTHORIZED)
		
		try:
			user = UserInfo.objects.get(id=token['user_id'])
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Couldn\'t find user',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_404_NOT_FOUND)
	
		if user.is_verified:
			return Response({
				'success': 'Email is already verified',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_200_OK)

		user.is_verified = True
		user.save()

		token.blacklist()

		return Response({
			'success': 'Email was verified successfully',
			'redirect': True,
			'redirect_url': '/api/login/'
		},
		status=status.HTTP_200_OK)