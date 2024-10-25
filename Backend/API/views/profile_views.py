
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import *
from ..serializers.user_serializer import *
from ..utils import Utils
from django.conf import settings
from rest_framework import serializers
from django.db.models import Q


class GetAllUsersView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		users = UserInfo.objects.exclude(is_superuser=True)
		return Response({
			'success': 'Users was retrieved successfully',
			'output': GetUserSerializer(users, many=True, context = {'request': request}).data
		},
		status=status.HTTP_200_OK)

class GetProfileView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request, username = None) -> Response:

		user = request.user

		if not user:
			return Response({
				'error': 'Couldn\'t find the user',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		if username:
			if user.username == username:
				return Response({
					'success': 'User was retrieved successfully',
					'output': GetUserSerializer(user,  context = {'request': request}).data
				})
			try:
				user = UserInfo.objects.get(username=username)
				return Response({
					'success': 'User retrieved successfully',
					'output': GetUserSerializer(user,  context = {'request': request}).data
				})
			except UserInfo.DoesNotExist:
				return Response({
					'error': 'User not found',
				},
				status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({
				'success': 'User retrieved successfully',
				'output': GetUserSerializer(user,  context = {'request': request}).data
			},
			status=status.HTTP_200_OK)


class ProfileUpdatingView(APIView):

	permission_classes = [IsAuthenticated]

	def put(self, request: Request) -> Response:

		serializer = ProfileUpdatingSerializer(instance=request.user,
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
	
class FriendOperationsView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:

		sender = request.data.get('sender')
		receiver = request.data.get('receiver')
		request_status = request.data.get('request_status')

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
		
		if sender != request.user.username:
			return Response({
				'error': 'You are not authorized to perform this action',
			},
			status=status.HTTP_403_FORBIDDEN)
		
		if sender == receiver:
			return Response({
				'error': 'You cannot send a friend request to yourself',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			receiver = UserInfo.objects.get(username=receiver)
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Receiver not found',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		serializer = FriendOperationsSerializer(data={
			'sender': sender.pk,
			'receiver': receiver.pk,
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

class FriendshipListView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		user = request.user

		print(user.username)

		if not user:
			return Response({
				'error': 'Couldn\'t find the user',
			},
			status=status.HTTP_404_NOT_FOUND)

		friendships = FriendshipLists.objects.filter(Q(user=user))

		return Response({
			'success': 'Friendships were retrieved successfully',
			'output': GetFriendshipListSerializer(friendships, many=True).data
		},
		status=status.HTTP_200_OK)

class FriendRequestsView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		user = request.user

		if not user:
			return Response({
				'error': 'Couldn\'t find the user',
			},
			status=status.HTTP_404_NOT_FOUND)

		friend_requests = FriendRequests.objects.filter(receiver=user)

		return Response({
			'success': 'Friend requests were retrieved successfully',
			'output': GetFriendRequestsListView(friend_requests, many=True).data
		},
		status=status.HTTP_200_OK)