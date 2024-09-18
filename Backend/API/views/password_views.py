from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from ..serializers import PasswordUpdateSerializer, ResetPasswordSerializer
from ..models import UserInfo
from rest_framework import serializers
from ..utils import Utils


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
				'error': 'Couldn\'t find the email',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_404_NOT_FOUND)

		tokens = Utils.create_jwt_for_user(user)
		absurl = f'http://127.0.0.1:3000/password-reset/?token={str(tokens["refresh_token"])}'

		email_body = f'Hi {user.username},\n\nPlease use the link below to reset your password:\n{absurl}'
		data = {
			'domain': absurl,
			'subject': 'Reset your password',
			'email': user.email,
			'body': email_body
		}

		Utils.send_verification_email(data)

		return Response({
			'success': 'Password reset email was sent',
			'user_id': user.id,
			'redirect': True,
			'redirect_url': '/api/login/'
		},
		status=status.HTTP_200_OK)

class PasswordVerify(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def post(self, request: Request) -> Response:

		token = request.GET.get('refresh_token')

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
		
		return Response({
			'success': "Token is valid",
			'redirect': False,
			'redirect_url': None
		},
		status=status.HTTP_200_OK)

class PasswordConfirmationView(APIView):

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