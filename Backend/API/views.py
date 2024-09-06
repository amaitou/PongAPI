
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
from rest_framework import status
from django.conf import settings
from django.urls import reverse
from .serializers import *
from rest_framework_simplejwt.tokens import AccessToken
from .utils import Utils
import requests

class RegisterView(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def post(self, request: Request) -> Response:

		serializer = UserRegistrationSerializer(data=request.data)

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

		tokens = Utils.create_jwt_for_user(serializer.instance)

		current_site = get_current_site(request).domain
		relative_link = reverse('email_verification')
		absurl = f'http://{current_site}{relative_link}?token={str(tokens["refresh_token"])}'
		email_body = f'Hi {serializer.instance.username},\n\nPlease use the link below to verify your email address:\n{absurl}'
		data = {
			'domain': absurl,
			'subject': 'Verify your email',
			'email': serializer.instance.email,
			'body': email_body
		}

		Utils.send_verification_email(data)

		return Response ({
			'success': 'User registered successfully, check your email for verification',
			'redirect': True,
			'redirect_url': '/api/login/',
			'data': serializer.data,
		},
		status=status.HTTP_201_CREATED)

class Authentication42View(APIView):

	permission_classes = [AllowAny]

	def get(self, request: Request) -> Response:

		if request.user.is_authenticated:
			return Response({
				'success': 'User already logged in',
				'redirect': True,
				'redirect_url': '/api/profile/'
			},
			status=status.HTTP_200_OK)
		
		code = request.GET.get('code')

		if not code:
			return Response({
				'error': 'No code provided',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		data = {
			'grant_type': 'authorization_code',
			'client_id': settings.CLIENT_ID,
			'client_secret': settings.CLIENT_SECRET,
			'code': code.encode('utf-8'),
			'redirect_uri': settings.REDIRECT,
		}

		__token = requests.post("https://api.intra.42.fr/oauth/token/", data=data)

		if not "access_token" in __token.json():
			return Response({
				'error': 'Invalid code',
				'redirect': True,
				'redirect_url': '/api/login/'
			},
			status=status.HTTP_400_BAD_REQUEST)
		
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

			response = Response({
				'success': 'User registered successfully',
				'redirect': True,
				'redirect_url': '/api/profile/',
				'data': serializer.data,
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

class LoginView(APIView):

	permission_classes = [AllowAny]

	def post(self, request: Request) -> Response:
		if request.user.is_authenticated:
			return Response({
				'success': 'User already logged in',
				'redirect': True,
				'redirect_url': f'/api/profile/'
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
		
		if not user.is_verified:
			return Response({
				'error': 'User is not verified, please check your email',
				'redirect': True,
				'redirect_url': '/api/login/',
			},
			status=status.HTTP_401_UNAUTHORIZED)

		response = Response({
			'success': 'Login successful',
			'redirect': True,
			'redirect_url': '/api/profile'
		},
		status=status.HTTP_200_OK)

		__jwt = Utils.create_jwt_for_user(user)

		response.set_cookie(settings.ACCESS_TOKEN, __jwt['access_token'], httponly=False)
		response.set_cookie(settings.REFRESH_TOKEN, __jwt['refresh_token'], httponly=True)

		return response

class LogoutView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		refresh = request.COOKIES.get(settings.REFRESH_TOKEN)

		if not refresh:
			return Response({
				'error': 'No refresh token is provided',
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


class AllUsersView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		users = UserInfo.objects.exclude(is_superuser=True)
		return Response({
			'success': 'Users was retrieved successfully',
			'redirect': False,
			'redirect_url': None,
			'data': GetUsersSerializer(users, many=True).data
		},
		status=status.HTTP_200_OK)

class ProfileView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request, username = None) -> Response:

		user = Utils.get_user_from_jwt(str(request.COOKIES.get(settings.ACCESS_TOKEN)), 'access')

		if not user:
			return Response({
				'error': 'Couldn\'t retrieve user from token',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_404_NOT_FOUND)
		
		if username:
			if user.username == username:
				return Response({
					'success': 'User retrieved successfully',
					'redirect': False,
					'redirect_url': None,
					'data': GetUserBasicInfoSerializer(user).data
				})
			try:
				user = UserInfo.objects.get(username=username)
				return Response({
					'success': 'User retrieved successfully',
					'redirect': False,
					'redirect_url': None,
					'data': GetUserBasicInfoSerializer(user).data
				})
			except UserInfo.DoesNotExist:
				return Response({
					'error': 'User not found',
					'redirect': False,
					'redirect_url': None
				},
				status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({
				'success': 'User retrieved successfully',
				'redirect': False,
				'redirect_url': None,
				'data': GetUserBasicInfoSerializer(user).data
			},
			status=status.HTTP_200_OK)

class PasswordUpdateView(APIView):

	permission_classes = [IsAuthenticated]

	def put(self, request: Request) -> Response:

		serializer = PasswordUpdateSerializer(instance=request.user,
					data=request.data,
					context={'request': request})

		try:
			serializer.is_valid(raise_exception=True)
		except serializers.ValidationError as e:
			return Response({
				'error': e.detail,
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_400_BAD_REQUEST)

		serializer.save()

		return Response({
			'success': 'Password updated successfully',
			'redirect': False,
			'redirect_url': None
		},
		status=status.HTTP_200_OK)

class ProfileUpdateView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:

		serializer = UserProfileSerializer(instance=request.user,
					data=request.data,
					context={'request': request},
					partial=True)
		try:
			serializer.is_valid(raise_exception=True)
		except serializers.ValidationError as e:
			return Response({
				'error': e.detail,
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_400_BAD_REQUEST)

		serializer.save()

		return Response({
			'success': 'Profile updated successfully',
			'redirect': False,
			'redirect_url': None
		},
		status=status.HTTP_200_OK)

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
				'error': 'Invalid or expired token',
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
				'success': 'Email already verified',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_200_OK)

		user.is_verified = True
		user.save()

		token.blacklist()

		return Response({
			'success': 'Email verified successfully',
			'redirect': True,
			'redirect_url': '/api/login/'
		},
		status=status.HTTP_200_OK)

class PasswordResetView(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def post(self, request: Request) -> Response:

		email = request.data.get('email')

		if not email:
			return Response({
				'error': 'No email provided',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			user = UserInfo.objects.get(email=email)
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Couldn\'t find the provided email',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_404_NOT_FOUND)

		tokens = Utils.create_jwt_for_user(user)
		current_site = get_current_site(request).domain
		relative_link = reverse('password_verification')
		absurl = f'http://{current_site}{relative_link}?token={str(tokens["refresh_token"])}'

		email_body = f'Hi {user.username},\n\nPlease use the link below to reset your password:\n{absurl}'
		data = {
			'domain': absurl,
			'subject': 'Reset your password',
			'email': user.email,
			'body': email_body
		}

		Utils.send_verification_email(data)

		return Response({
			'success': 'Password reset email sent',
			'redirect': True,
			'redirect_url': '/api/login/'
		},
		status=status.HTTP_200_OK)

class PasswordVerifyView(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def post(self, request: Request) -> Response:

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
				'error': 'Invalid or expired token',
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

		serializer = ResetPasswordSerializer(instance=user, data=request.data)
		try:
			serializer.is_valid(raise_exception=True)
		except serializers.ValidationError as e:
			return Response({
				'error': e.detail,
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_400_BAD_REQUEST)

		serializer.save()
		token.blacklist()

		return Response({
			'success': 'Password reset successfully',
			'redirect': True,
			'redirect_url': '/api/login/'
		},
		status=status.HTTP_200_OK)