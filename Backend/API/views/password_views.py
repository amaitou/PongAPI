from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.password_serializer import *
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from django.conf import settings
from ..models import UserInfo
from ..utils import Utils
import jwt


class PasswordUpdatingView(APIView):

	permission_classes = [IsAuthenticated]

	def put(self, request: Request) -> Response:

		serializer = PasswordUpdatingSerializer(instance=request.user,
					data=request.data,
					context={'request': request})

		try:
			serializer.is_valid(raise_exception=True)
		except serializers.ValidationError as e:
			return Response({
				'error': e.detail,
			},
			status=status.HTTP_400_BAD_REQUEST)

		serializer.save()

		return Response({
			'success': 'Password updated successfully',
		},
		status=status.HTTP_200_OK)

class PasswordResettingView(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def post(self, request: Request) -> Response:

		email = request.data.get('email')

		if not email:
			return Response({
				'error': 'No email provided',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			user = UserInfo.objects.get(email=email)
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Couldn\'t find the email',
			},
			status=status.HTTP_404_NOT_FOUND)

		verification_token = Utils.create_one_time_jwt(user)
		absurl = f'http://127.0.0.1:3000/password-reset/?token={verification_token}'

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
		},
		status=status.HTTP_200_OK)

class PasswordVerificationView(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def post(self, request: Request) -> Response:

		verification_token = request.GET.get('token')

		if not verification_token:
			return Response({
				'error': 'No token provided',
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
		
		try:
			user = UserInfo.objects.get(id=token['user_id'])
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Couldn\'t find user',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		return Response({
			'success': "Token is valid",
		},
		status=status.HTTP_200_OK)

class PasswordConfirmationView(APIView):

	permission_classes = [AllowAny]
	authentication_classes = []

	def post(self, request: Request) -> Response:

		verification_token = request.GET.get('token')

		if not verification_token:
			return Response({
				'error': 'No token provided',
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
	

		try:
			user = UserInfo.objects.get(id=token['user_id'])
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Couldn\'t find user',
			},
			status=status.HTTP_404_NOT_FOUND)

		serializer = PasswordResettingSerializer(instance=user, data=request.data)
		try:
			serializer.is_valid(raise_exception=True)
		except serializers.ValidationError as e:
			return Response({
				'error': e.detail,
			},
			status=status.HTTP_400_BAD_REQUEST)

		serializer.save()

		return Response({
			'success': 'Password reset successfully',
		},
		status=status.HTTP_200_OK)