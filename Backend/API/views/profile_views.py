
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import UserInfo
from ..serializers import UserSerializer, ProfileUpdateSerializer
from ..utils import Utils
from django.conf import settings
from rest_framework import serializers

class AllUsersView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		users = UserInfo.objects.exclude(is_superuser=True)
		return Response({
			'success': 'Users was retrieved successfully',
			'redirect': False,
			'redirect_url': None,
			'data': UserSerializer(users, many=True).data
		},
		status=status.HTTP_200_OK)

class ProfileView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request, username = None) -> Response:

		user = Utils.get_user_from_jwt(str(request.COOKIES.get(settings.ACCESS_TOKEN)), 'access')

		if not user:
			return Response({
				'error': 'Couldn\'t find the user',
				'redirect': False,
				'redirect_url': None
			},
			status=status.HTTP_404_NOT_FOUND)
		
		if username:
			if user.username == username:
				return Response({
					'success': 'User was retrieved successfully',
					'redirect': False,
					'redirect_url': None,
					'data': UserSerializer(user).data
				})
			try:
				user = UserInfo.objects.get(username=username)
				return Response({
					'success': 'User retrieved successfully',
					'redirect': False,
					'redirect_url': None,
					'data': UserSerializer(user).data
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
				'data': UserSerializer(user).data
			},
			status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):

	permission_classes = [IsAuthenticated]

	def put(self, request: Request) -> Response:

		serializer = ProfileUpdateSerializer(instance=request.user,
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
			'success': 'Profile was updated successfully',
			'redirect': False,
			'redirect_url': None
		},
		status=status.HTTP_200_OK)