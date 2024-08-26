
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .models import UserInfo, UserGameStats
from rest_framework.request import Request
from rest_framework.views import APIView
from .verification import Verification
from rest_framework import status
from django.conf import settings
from django.urls import reverse
from .serializers import *
from .jwt import *
import requests

class RegisterView(APIView):

	permission_classes = [AllowAny]

	def post(self, request: Request) -> Response:

		serializer = UserRegistrationSerializer(data=request.data)

		try:
			serializer.is_valid(raise_exception=True)
			serializer.save()

			tokens = create_jwt_for_user(serializer.instance)
			current_site = get_current_site(request).domain
			relative_link = reverse('email_verification')
			absurl = f'http://{current_site}{relative_link}?token={str(tokens["access_token"])}'
			email_body = f'Hi {serializer.instance.username},\n\nPlease use the link below to verify your email address:\n{absurl}'
			data = {
				'domain': absurl,
				'subject': 'Verify your email',
				'email': serializer.instance.email,
				'body': email_body
			}

			Verification.send_verification_email(data)

			response = Response ({
				'message': 'User registered successfully',
				'redirect': True,
				'redirect_url': '/api/login/',
				'data': serializer.data,
				'jwt': tokens
			},
			status=status.HTTP_201_CREATED)

			return response

		except serializers.ValidationError as e:
			return Response({
				'message': e.detail,
				'redirect': False,
				'redirect_url': ''
			},
			status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

	permission_classes = [AllowAny]

	def post(self, request: Request) -> Response:
		if request.user.is_authenticated:
			return Response({
				'message': 'User already logged in',
				'redirect': True,
				'redirect_url': '/api/profile/',
			},
			status=status.HTTP_200_OK)

		username = request.data.get("username")
		password = request.data.get("password")

		user = authenticate(request, username=username, password=password)

		if not user:
			return Response({
				'message': 'Invalid credentials',
				'redirect': False,
				'redirect_url': '',
			},
			status=status.HTTP_401_UNAUTHORIZED)
		
		if not user.is_verified:
			return Response({
				'message': 'User not verified',
				'redirect': False,
				'redirect_url': '',
			},
			status=status.HTTP_401_UNAUTHORIZED)

		response = Response({
			'message': 'Login successful',
			'redirect': True,
			'redirect_url': '/api/profile',
			'jwt': create_jwt_for_user(user)
		},
		status=status.HTTP_200_OK)

		return response

class LogoutView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:

		refresh = request.data.get(settings.REFRESH_TOKEN)
		print(refresh)
		if not refresh:
			return Response({
				'message': 'No refresh token provided',
				'redirect': False,
				'redirect_url': ''
			},
			status=status.HTTP_400_BAD_REQUEST)

		try:
			token = RefreshToken(refresh)
			token.blacklist()
		except TokenError:
			return Response({
				'message': 'Refresh token is invalid, expired or blacklisted',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_401_UNAUTHORIZED)

		response = Response({
			'message': 'Logout successful',
			'redirect': True,
			'redirect_url': '/api/login/'
		},
		status=status.HTTP_200_OK)

		return response

class Authentication42(APIView):

	permission_classes = [AllowAny]

	def get(self, request: Request) -> Response:

		if request.user.is_authenticated:
			return Response({
				'message': 'User already logged in',
				'redirect': True,
				'redirect_url': '/api/profile/'
			}, status=status.HTTP_200_OK)
		
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
		avatar = user['image']['link']

		serializer = UserRegistrationSerializer(data={
			'username': username,
			'first_name': first_name,
			'last_name': last_name,
			'email': email
		})

		if serializer.is_valid():
			serializer.save()

			tokens = create_jwt_for_user(serializer.instance)
			access_token = tokens['access_token']
			refresh_token = tokens['refresh_token']

			response = Response({
				'message': 'User registered successfully',
				'redirect': True,
				'redirect_url': '/api/login/',
				'data': serializer.data,
			}, status=status.HTTP_201_CREATED)

			response.set_cookie(settings.ACCESS_TOKEN, access_token)
			response.set_cookie(settings.REFRESH_TOKEN, refresh_token, httponly=True)

			return response
		else:
			try:
				user = UserInfo.objects.get(username=username)
			except UserInfo.DoesNotExist:
				return Response({
					'message': 'Invalid data',
					'redirect': False,
					'redirect_url': ''
				}, status=status.HTTP_400_BAD_REQUEST)
			
			response = Response({
				'message': 'Login successful',
				'redirect': True,
				'redirect_url': '/api/profile'
			}, status=status.HTTP_200_OK)

			tokens = create_jwt_for_user(user)
			access_token = tokens['access_token']
			refresh_token = tokens['refresh_token']

			response.set_cookie(settings.ACCESS_TOKEN, access_token)
			response.set_cookie(settings.REFRESH_TOKEN, refresh_token, httponly=True)

			return response

class TokenRefresher(APIView):

	permission_classes = [AllowAny]

	def post(self, request: Request) -> Response:

		refresh = request.data.get(settings.REFRESH_TOKEN)

		if not refresh:
			return Response({
				'message': 'No refresh token provided',
				'redirect': False,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_400_BAD_REQUEST)

		try:
			token = RefreshToken(refresh)
			token.blacklist()
		except TokenError:
			return Response({
				'message': 'Refresh token is invalid or expired',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_401_UNAUTHORIZED)

		user = UserInfo.objects.get(id=token['user_id'])

		if not user:
			return Response({
				'message': 'User not found',
				'redirect': False,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_404_NOT_FOUND)

		response = Response({
			'message': 'Token refreshed',
			'redirect': True,
			'redirect_url': '/api/profile',
			'jwt': create_jwt_for_user(user)
		},
		status=status.HTTP_200_OK)

		return response

class AllUsersView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		users = UserInfo.objects.filter(id__gt=1)
		return Response({
			'message': 'Users retrieved successfully',
			'redirect': False,
			'redirect_url': '',
			'data': GetUsersSerializer(users, many=True).data
		},
		status=status.HTTP_200_OK)

class ProfileView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request, username = None) -> Response:

		user = request.user
		
		if username:
			if user.username == username:
				return Response({
					'message': 'User retrieved successfully',
					'redirect': False,
					'redirect_url': '',
					'data': GetUserBasicInfoSerializer(user).data
				})
			try:
				user = UserInfo.objects.get(username=username)
				return Response({
					'message': 'User retrieved successfully',
					'redirect': False,
					'redirect_url': '',
					'data': GetUserBasicInfoSerializer(user).data
				})
			except UserInfo.DoesNotExist:
				return Response({
					'message': 'User not found',
					'redirect': False,
					'redirect_url': ''
				},
				status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({
			'message': 'User retrieved successfully',
			'redirect': False,
			'redirect_url': '',
			'data': GetUserBasicInfoSerializer(user).data
			},
			status=status.HTTP_200_OK)

class UpdatePasswordView(APIView):

	permission_classes = [IsAuthenticated]

	def put(self, request: Request) -> Response:

		serializer = PasswordUpdateSerializer(instance=request.user, data=request.data, context={'request': request})

		try:
			serializer.is_valid(raise_exception=True)
			serializer.save()
			response = Response({
				'message': 'Password updated successfully',
				'redirect': False,
				'redirect_url': ''
			},
			status=status.HTTP_200_OK)
			return response
		except serializers.ValidationError as e:
			response = Response({
				'message': e.detail,
				'redirect': False,
				'redirect_url': ''
			},
			status=status.HTTP_400_BAD_REQUEST)
			return response