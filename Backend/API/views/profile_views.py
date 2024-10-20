
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import UserInfo
from ..serializers.user_serializer import UserSerializer, ProfileUpdateSerializer, FriendshipSerializer
from ..utils import Utils
from django.conf import settings
from rest_framework import serializers

class AllUsersView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		users = UserInfo.objects.exclude(is_superuser=True)
		return Response({
			'success': 'Users was retrieved successfully',
			'output': UserSerializer(users, many=True, context = {'request': request}).data
		},
		status=status.HTTP_200_OK)

class ProfileView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request, username = None) -> Response:

		user = Utils.get_user_from_jwt(str(request.COOKIES.get(settings.ACCESS_TOKEN)), 'access')

		if not user:
			return Response({
				'error': 'Couldn\'t find the user',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		if username:
			if user.username == username:
				return Response({
					'success': 'User was retrieved successfully',
					'output': UserSerializer(user,  context = {'request': request}).data
				})
			try:
				user = UserInfo.objects.get(username=username)
				return Response({
					'success': 'User retrieved successfully',
					'output': UserSerializer(user,  context = {'request': request}).data
				})
			except UserInfo.DoesNotExist:
				return Response({
					'error': 'User not found',
				},
				status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({
				'success': 'User retrieved successfully',
				'output': UserSerializer(user,  context = {'request': request}).data
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
			},
			status=status.HTTP_400_BAD_REQUEST)

		serializer.save()

		return Response({
			'success': 'Profile was updated successfully',
		},
		status=status.HTTP_200_OK)
	
class FriendshipView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:

		sender = request.data.get('sender')
		receiver = request.data.get('receiver')
		request_status = request.data.get('request_status')

		print(sender, receiver, request_status)

		if not sender or not receiver or not request_status:
			return Response({
				'error': 'Please provide all the required fields',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			sender = UserInfo.objects.get(username=sender)
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Sender not found',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		try:
			receiver = UserInfo.objects.get(username=receiver)
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Receiver not found',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		serializer = FriendshipSerializer(data={
			'sender_id': sender.pk,
			'receiver_id': receiver.pk,
			'request_status': request_status
		})

		try:
			serializer.is_valid(raise_exception=True)
		except serializers.ValidationError as e:
			return Response({
				'error': e.detail,
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		serializer.save()

		return Response({
			'success': 'Friendship was handled successfully',
		},
		status=status.HTTP_200_OK)