
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.user_serializer import *
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from django.conf import settings
from django.db.models import Q
from ..utils import Utils
from ..models import *


class GetAllUsersView(APIView):

	"""
    View to retrieve all users excluding superusers.
    This endpoint is accessible only to authenticated users.
    """

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		users = UserInfo.objects.exclude(is_superuser=True)
		total_users = users.count()
		return Response({
			'success': 'Users was retrieved successfully',
			'total_users': total_users,
			'users': GetUsersListSerializer(users, many=True, context = {'request': request}).data
		},
		status=status.HTTP_200_OK)

class GetProfileView(APIView):

	"""
    View to retrieve the profile details of a user.
    It allows fetching the profile of the currently logged-in user,
    or any other user by specifying their username in the URL.
    """

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
					'user': GetUserFullData(user,  context = {'request': request}).data
				})
			try:
				user = UserInfo.objects.get(username=username)
				return Response({
					'success': 'User retrieved successfully',
					'user': GetUserFullData(user,  context = {'request': request}).data
				})
			except UserInfo.DoesNotExist:
				return Response({
					'error': 'User not found',
				},
				status=status.HTTP_404_NOT_FOUND)
		else:
			return Response({
				'success': 'User retrieved successfully',
				'user': GetUserFullData(user,  context = {'request': request}).data
			},
			status=status.HTTP_200_OK)


class ProfileUpdatingView(APIView):

	"""
    View to update the profile information of the currently authenticated user.
    This supports partial updates and only requires the fields provided in the request.
    """

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

	"""
    View to handle friend request operations such as sending, accepting, declining, and deleting requests.
    The sender and receiver must be specified, and the operation type must be provided in the request.
    """

	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:

		sender = request.data.get('sender')
		receiver = request.data.get('receiver')
		request_status = request.data.get('request_status')
		user = request.user

		if not sender or not receiver or not request_status:
			return Response({
				'error': 'Please provide all the required fields',
			},
			status=status.HTTP_400_BAD_REQUEST)
	
		if request.user.username != sender:
			return Response({
				'error': 'You are not authorized to send this request',
			},
			status=status.HTTP_401_UNAUTHORIZED)
		
		try:
			sender = UserInfo.objects.get(username=sender)
		except UserInfo.DoesNotExist:
			return Response({
				'error': 'Sender not found',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		if sender == receiver:
			return Response({
				'error': 'You cannot send a friend request to yourself',
			},
			status=status.HTTP_400_BAD_REQUEST)
		
		try:
			receiver = UserInfo.objects.get(username=receiver)
		except UserInfo.DoesNotExist:
			return Response({
				'message': 'Receiver not found',
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

		if request_status == 'A':
			return Response({
				'success': 'Friend request was accepted successfully',
			},
			status=status.HTTP_200_OK)
		elif request_status == 'P':
			return Response({
				'success': 'Friend request was sent successfully',
			},
			status=status.HTTP_200_OK)
		elif request_status == 'D':
			return Response({
				'success': 'Friend request was declined successfully',
			},
			status=status.HTTP_200_OK)
		else:
			return Response({
				'success': 'Friend request was deleted successfully',
			},
			status=status.HTTP_200_OK)

class FriendshipListView(APIView):

	"""
    View to retrieve a list of friends of the currently authenticated user.
    This endpoint will return all the friendships where the user is involved.
    """

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		user = request.user

		if not user:
			return Response({
				'error': 'Couldn\'t find the user',
			},
			status=status.HTTP_404_NOT_FOUND)

		friendships = FriendshipLists.objects.filter(user=user)
		total_friends = friendships.count()

		return Response({
			'success': 'Friendships were retrieved successfully',
			'total_friends': total_friends,
			'friends': GetFriendshipListSerializer(friendships, many=True).data
		},
		status=status.HTTP_200_OK)

class FriendRequestsView(APIView):

	"""
    View to retrieve all the friend requests that have been received by the currently authenticated user.
    """

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		user = request.user

		if not user:
			return Response({
				'error': 'Couldn\'t find the user',
			},
			status=status.HTTP_404_NOT_FOUND)

		friend_requests = FriendRequests.objects.filter(receiver=user)
		total_requests = friend_requests.count()

		return Response({
			'success': 'Friend requests were retrieved successfully',
			'total_requests': total_requests,
			'requests': GetFriendRequestsSerializer(friend_requests, many=True).data
		},
		status=status.HTTP_200_OK)

class SentRequestsView(APIView):

	"""
    View to retrieve all the friend requests that have been sent by the currently authenticated user.
    """

	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:

		user = request.user

		if not user:
			return Response({
				'error': 'Couldn\'t find the user',
			},
			status=status.HTTP_404_NOT_FOUND)
		
		sent_requests = FriendRequests.objects.filter(sender=user)
		total_requests = sent_requests.count()

		return Response({
			'success': 'Sent requests were retrieved successfully',
			'total_requests': total_requests,
			'requests': SentRequestsSerializer(sent_requests, many=True).data
		},
		status=status.HTTP_200_OK)