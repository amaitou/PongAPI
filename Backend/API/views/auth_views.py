
from ..serializers.user_serializer import GetBasicUserInfoSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..serializers.user_serializer import RegistrationSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
from ..models import UserGameStats
from django.utils import timezone
from rest_framework import status
from django.conf import settings
from django.urls import reverse
from ..models import UserInfo
from ..utils import Utils
import requests
import jwt

class RegistrationView(APIView):

	"""
	This view handles user registration by accepting user data via a POST request, 
	validating it using the RegistrationSerializer, and saving the user details. 
	After registration, it creates associated game statistics for the user and sends 
	an email verification link containing a one-time JWT for account confirmation.
	"""

	permission_classes = [AllowAny]
	authentication_classes = []

	def create_unique_username(self, original_username):
		"""
		This method creates a unique username by appending a counter to the original username.
		"""
		base_username = original_username
		counter = 1
		while UserInfo.objects.filter(username=original_username).exists():
			original_username = f"{base_username}_{counter}"
			counter += 1
		
		return original_username

	def post(self, request: Request) -> Response:

		registration_data = request.data.copy()
		current_username = registration_data.get('username')

		if current_username and UserInfo.objects.filter(username=current_username).exists():
			registration_data['username'] = self.create_unique_username(current_username)

		serializer = RegistrationSerializer(data=registration_data,
				context={'request': request})

		try:
			serializer.is_valid(raise_exception=True)
		except serializers.ValidationError as e:
			return Response({
				'error': e.detail[Utils.retrieve_key_from_serializer_error(e)],
			},
			status=status.HTTP_400_BAD_REQUEST)

		serializer.save()

		user_game_stats = UserGameStats.objects.create(user_id = serializer.instance)
		user_game_stats.save()

		token = Utils.create_one_time_jwt(serializer.instance, "email_verification")

		# current_site = get_current_site(request).domain
		# relative_link = reverse('email_verification')
		# absurl = f'http://{current_site}{relative_link}?token={str(token)}'
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
			'user': serializer.data,
		},
		status=status.HTTP_201_CREATED)

class Authentication42View(APIView):

	"""
	The Authentication42View is a Django REST Framework view that handles OAuth authentication with 42's authentication service.
	It provides a streamlined process for user registration and login using 42's OAuth credentials.
	"""
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
		token = requests.post("https://api.intra.42.fr/oauth/token/", data=self.data)
		if not "access_token" in token.json():
			return None
		return token.json()['access_token']

	def __get_user(self, access_token: str) -> dict:
		user = requests.get("https://api.intra.42.fr/v2/me", headers={
			'Authorization': f'Bearer {access_token}'
		})
		return user.json()
	
	def __set_code_in_data(self, code: str) -> None:
		self.data['code'] = code.encode('utf-8')

	def __generate_unique_username(self, base_username: str) -> str:
		"""Generate a unique username by appending numbers if the base username exists."""
		username = base_username
		counter = 1
		
		while UserInfo.objects.filter(username=username).exists():
			username = f"{base_username}{counter}"
			counter += 1
			
		return username

	def __process_avatar(self, avatar_url: str) -> SimpleUploadedFile:
		"""Process and return avatar file from URL."""
		requested_avatar = requests.get(avatar_url)
		avatar_name = avatar_url.split('/')[-1]
		return SimpleUploadedFile(avatar_name, requested_avatar.content, content_type='image/jpg')

	def __create_response(self, user: UserInfo) -> HttpResponseRedirect:
		"""Create HTTP response with JWT tokens."""
		response = HttpResponseRedirect('https://127.0.0.1/')
		jwt = Utils.create_jwt_for_user(user)
		
		response.set_cookie(
			settings.ACCESS_TOKEN, 
			jwt['access_token'], 
			httponly=False, 
			secure=True, 
			samesite='None'
		)
		response.set_cookie(
			settings.REFRESH_TOKEN, 
			jwt['refresh_token'], 
			httponly=True, 
			secure=True, 
			samesite='None'
		)
		
		return response

	def __register_user(self, user: dict, request: Request) -> HttpResponseRedirect:
		first_name = user['first_name']
		last_name = user['last_name']
		base_username = user['login']
		email = user['email']
		avatar_url = user['image']['link']

		existing_user = UserInfo.objects.filter(email=email).first()
		if existing_user:
			return self.__create_response(existing_user)

		username = self.__generate_unique_username(base_username)
		avatar = self.__process_avatar(avatar_url)

		user_data = {
			'username': username,
			'first_name': first_name,
			'last_name': last_name,
			'email': email,
			'gender': 'M',
			'avatar': avatar,
		}

		serializer = RegistrationSerializer(
			data=user_data, 
			context={'request': request}
		)

		if serializer.is_valid():
			user = serializer.save()
			user.is_verified = True
			user.save()

			UserGameStats.objects.create(user_id=user)

			return self.__create_response(user)
		
		return Response(
			{'error': 'Failed to register user', 'details': serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)

	def get(self, request: Request) -> Response:
		if request.user.is_authenticated:
			return Response({
				'success': 'User already logged in',
				'user': GetBasicUserInfoSerializer(request.user).data
			},
			status=status.HTTP_200_OK)
		
		self.code = self.__get_code(request)
		self.__set_code_in_data(self.code)

		if not self.code:
			return Response({
				'error': 'No code was provided',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		access_token = self.__get_token()

		if not access_token:
			return Response({
				'error': 'Failed to authenticate',
			},
			status=status.HTTP_400_BAD_REQUEST)

		user = self.__get_user(access_token)
		return self.__register_user(user, request)

class LoginConfirmationView(APIView):

	"""
	This view handles user login by accepting a username and password via a POST request. 
	It authenticates the user and generates JWT tokens. If two-factor authentication (2FA) 
	is enabled for the user, it sends a one-time password (OTP) to their email. If 2FA is 
	not enabled, the view completes the login process and sets tokens in cookies.
	"""

	permission_classes = [AllowAny]

	def post(self, request: Request) -> Response:
		if request.user.is_authenticated:
			return Response({
				'success': 'User already logged in',
				'user': GetBasicUserInfoSerializer(request.user, context = {'request': request}).data,
			},
			status=status.HTTP_200_OK)

		email = request.data.get("email")
		password = request.data.get("password")

		user = authenticate(request, email=email, password=password)

		if not user:
			return Response({
				'error': 'Invalid email or password',
			},
			status=status.HTTP_401_UNAUTHORIZED)
		
		# if not user.is_verified:
		# 	return Response({
		# 		'error': 'User is not verified, check your email',
		# 	},
		# 	status=status.HTTP_401_UNAUTHORIZED)
		
		if not user.two_fa:
			response = Response({
				'success': 'Login successful',
				'user': GetBasicUserInfoSerializer(user, context = {'request': request}).data
			},
			status=status.HTTP_200_OK)

			__jwt = Utils.create_jwt_for_user(user)

			response.set_cookie(settings.ACCESS_TOKEN,
					__jwt['access_token'],
					httponly=True,
					secure= Utils.set_protocol(),
					samesite=Utils.set_cross_origin_value())

			response.set_cookie(settings.REFRESH_TOKEN,
					__jwt['refresh_token'],
					httponly=True,
					secure= Utils.set_protocol(),
					samesite=Utils.set_cross_origin_value())

			return response
		
		user.otp_code = Utils.generate_otp_code()
		user.otp_time = Utils.generate_otp_expiration()

		absurl = f''
		email_body = f'Hi {user.username},\n\nPlease use the code below to verify your login:\n{user.otp_code}'
		data = {
			'domain': absurl,
			'subject': 'Verification code',
			'email': user.email,
			'body': email_body
		}

		Utils.send_verification_email(data)

		user.save()

		token = Utils.create_one_time_jwt(user, "login_verification")

		response = Response({
			'success': "check your email for verification code",
		},
		status=status.HTTP_200_OK)

		response.set_cookie("verification_token", str(token),
				httponly=True,
				secure=Utils.set_protocol(),
				samesite=Utils.set_cross_origin_value())

		return response

class TwoFactorAuthenticationView(APIView):

	"""
	This view handles two-factor authentication (2FA) verification during login. It accepts 
	an OTP and a verification token via a POST request, verifies the provided credentials, 
	and completes the login process upon successful verification. Once verified, JWT tokens 
	are set in cookies for the authenticated user.
	"""

	permission_classes = [AllowAny]

	def post(self, request: Request) -> Response:

		if request.user.is_authenticated:
			return Response({
				'success': 'User already logged in',
				'user': GetBasicUserInfoSerializer(request.user).data
			},
			status=status.HTTP_200_OK)

		otp_code = request.data.get('otp_code')
		verification_token = request.COOKIES.get('verification_token')

		if not verification_token:
			return Response({
				'error': 'No verification token was provided',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		if not otp_code:
			return Response({
				'error': 'No otp code was provided',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			token = jwt.decode(verification_token, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			return Response({
				'error': 'Token is expired',
			},
			status=status.HTTP_400_BAD_REQUEST)
		except jwt.InvalidTokenError:
			return Response({
				'error': 'Token is invalid',
			},
			status=status.HTTP_400_BAD_REQUEST)
	
		if token['purpose'] != 'login_verification':
			return Response({
				'error': 'Invalid token purpose',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			user = UserInfo.objects.get(id=token['user_id'])
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Couldn\'t find user',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		if user.otp_code != otp_code:
			return Response({
				'error': 'Invalid otp code',
			},
			status=status.HTTP_401_UNAUTHORIZED)
		
		if user.otp_time < timezone.now():
			return Response({
				'error': 'OTP code has expired',
			},
			status=status.HTTP_401_UNAUTHORIZED)
		
		user.otp_code = None
		user.otp_time = None
		user.save()

		response = Response({
			'success': 'Login successful',
			'user': GetBasicUserInfoSerializer(user).data
		},
		status=status.HTTP_200_OK)

		__jwt = Utils.create_jwt_for_user(user)

		response.set_cookie(settings.ACCESS_TOKEN,
					__jwt['access_token'],
					httponly=True,
					secure= Utils.set_protocol(),
					samesite=Utils.set_cross_origin_value())

		response.set_cookie(settings.REFRESH_TOKEN,
				__jwt['refresh_token'],
				httponly=True,
				secure= Utils.set_protocol(),
				samesite=Utils.set_cross_origin_value())

		response.delete_cookie('verification_token')

		return response

class LogoutView(APIView):

	"""
	This view handles user logout by accepting a POST request. It retrieves the refresh 
	token from cookies, validates it, and blacklists it to prevent further use. If the 
	token is invalid, expired, or not provided, the view returns an appropriate error 
	response. Upon successful logout, the access and refresh tokens are removed from cookies.
	"""

	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:

		refresh = request.COOKIES.get(settings.REFRESH_TOKEN)

		if not refresh:
			return Response({
				'error': 'No refresh token was provided',
			},
			status=status.HTTP_400_BAD_REQUEST)

		try:
			token = RefreshToken(refresh)
			token.blacklist()
		except TokenError:
			return Response({
				'error': 'Refresh token is invalid, expired or blacklisted',
			},
			status=status.HTTP_401_UNAUTHORIZED)

		response = Response({
			'success': 'Logout successful',
		},
		status=status.HTTP_200_OK)

		response.delete_cookie(settings.ACCESS_TOKEN)
		response.delete_cookie(settings.REFRESH_TOKEN)

		return response

class EmailVerificationView(APIView):

	"""
	This view manages email verification via a GET request containing a verification 
	token as a query parameter. It decodes and validates the token, checking its purpose 
	and expiration status. If valid, it retrieves the user associated with the token, 
	verifies their email, and updates their verification status in the database. 
	Appropriate error responses are returned for missing, invalid, or expired tokens, 
	as well as if the user cannot be found.
	"""

	permission_classes = [AllowAny]
	authentication_classes = []

	def get(self, request: Request) -> Response:

		token = request.query_params.get('token')

		if not token:
			return Response({
				'error': 'No token provided',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.ExpiredSignatureError:
			return Response({
				'error': 'Token is expired',
			},
			status=status.HTTP_400_BAD_REQUEST)
		except jwt.InvalidTokenError:
			return Response({
				'error': 'Token is invalid',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		if token['purpose'] != 'email_verification':
			return Response({
				'error': 'Invalid token purpose',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		if token['purpose'] != 'email_verification':
			return Response({
				'error': 'Invalid token purpose',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			user = UserInfo.objects.get(id=token['user_id'])
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Couldn\'t find user',
			},
			status=status.HTTP_404_NOT_FOUND)
			
		if user.is_verified:
			return Response({
				'success': 'Email is already verified',
			},
			status=status.HTTP_200_OK)

		user.is_verified = True
		user.save()

		return Response({
			'success': 'Email was verified successfully',
		},
		status=status.HTTP_200_OK)