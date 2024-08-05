from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import *

@csrf_exempt
def Register(request):

	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password1')
		password2 = request.POST.get('password2')
		date_joined = request.POST.get('date_joined')
		gender = request.POST.get("gender")
	
		if password == password2:
			user = PlayerInfo.objects.create(username=username,
							email=email,
							password=make_password(password),
							date_joined=date_joined,
							first_name=first_name,
							last_name=last_name,
							gender=gender)
			user.save()
			return JsonResponse({'status': 'success', 'message': 'User created successfully!'})
		else:
			return JsonResponse({'status': 'failed', 'message': 'Password does not match!'})

@csrf_exempt
def Login(request):
	
	if request.method == 'POST':

		if request.user.is_authenticated:
			return JsonResponse({'status': 'failed', 'message': 'User already logged in!'})
		username = request.POST.get('username')
		password = request.POST.get('password')
		if check_password(password, PlayerInfo.objects.get(username=username).password):
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return JsonResponse({'status': 'success', 'message': 'User logged in successfully!'})
			else:
				return JsonResponse({'status': 'failed', 'message': 'User not found!'})
		else:
			return JsonResponse({'status': 'failed', 'message': 'Incorrect password!'})

@csrf_exempt
def Logout(request):
	
	if request.method == 'POST':
		if request.user.is_authenticated:
			logout(request)
			return JsonResponse({'status': 'success', 'message': 'User logged out successfully!'})
		else:
			return JsonResponse({'status': 'failed', 'message': 'User not logged in!'})