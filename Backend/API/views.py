from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from .serializers import *
from django.http import JsonResponse
from .models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token

@api_view(['GET'])
def Routes(request):
	# Routes
	routes = [
		'/api/register',
		'/api/login',
		'/api/logout',
		'/api/delete',
	]
	return Response(routes)
	
@api_view(['POST'])
def Register(request):

	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		date_joined = request.POST.get('date_joined')
		gender = request.POST.get("gender")

		if PlayerInfo.objects.filter(username=username).exists():
			return Response({'status': 'failed', 'message': 'Username already exists!'})

		if password1 != password2:
			return Response({'status': 'failed', 'message': 'Password does not match!'})

		user = PlayerInfo.objects.create(username=username,
						email=email,
						password=make_password(password1),
						date_joined=date_joined,
						first_name=first_name,
						last_name=last_name,
						gender=gender)
		user.save()
	return Response({'status': 'success', 'message': 'User created successfully!'})


@api_view(['POST'])
def Login(request):
	
	if request.method == 'POST':

		username = request.data['username']
		print(username)
		if not PlayerInfo.objects.filter(username=username).exists():
			return Response({'status': 'failed', 'message': 'User not found!'})

		if request.user.is_authenticated:
			return Response({'status': 'failed', 'message': 'User already logged in!'})

		password = request.data['password']
		if not check_password(password, PlayerInfo.objects.get(username=username).password):
			return Response({'status': 'failed', 'message': 'Incorrect password!'})
		
		token = RefreshToken.for_user(PlayerInfo.objects.get(username=username))
		login(request, PlayerInfo.objects.get(username=username))
		return Response({'status': 'success', 'message': 'User logged in successfully!', 'token': str(token.access_token), 'refresh': str(token)})

@api_view(['POST'])
def Logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'status': 'success', 'message': 'User logged out successfully!'})
    except Exception as e:
        return Response({'status': 'failed', 'message': str(e)}, status=400)			


@api_view(['POST'])
def Delete(request):

	if request.method == 'POST':

		username = request.POST.get('username')
		if not PlayerInfo.objects.filter(username=username).exists():
			return JsonResponse({'status': 'failed', 'message': 'User not found!'})

		user = PlayerInfo.objects.get(username=username)
		user.delete()
		return JsonResponse({'status': 'success', 'message': 'User deleted successfully!'})

@api_view(['POST'])
def GetUser(request):
	users = PlayerInfo.objects.get(username=request.data['username'])
	__serializer = PlayerInfoSerializer(users)
	return Response(__serializer.data)