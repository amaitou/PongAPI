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
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		date_joined = request.POST.get('date_joined')
		gender = request.POST.get("gender")

		if PlayerInfo.objects.filter(username=username).exists():
			return JsonResponse({'status': 'failed', 'message': 'Username already exists!'})

		else:
			if password1 != password2:
				return JsonResponse({'status': 'failed', 'message': 'Password does not match!'})

			user = PlayerInfo.objects.create(username=username,
							email=email,
							password=make_password(password1),
							date_joined=date_joined,
							first_name=first_name,
							last_name=last_name,
							gender=gender)
			user.save()
	return JsonResponse({'status': 'success', 'message': 'User created successfully!'})

@csrf_exempt
def Login(request):
	
	if request.method == 'POST':

		username = request.POST.get('username')
		if not PlayerInfo.objects.filter(username=username).exists():
			return JsonResponse({'status': 'failed', 'message': 'User not found!'})

		if request.user.is_authenticated:
			return JsonResponse({'status': 'failed', 'message': 'User already logged in!'})

		password = request.POST.get('password')
		if not check_password(password, PlayerInfo.objects.get(username=username).password):
			return JsonResponse({'status': 'failed', 'message': 'Incorrect password!'})
		
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return JsonResponse({'status': 'success', 'message': 'User logged in successfully!'})

@csrf_exempt
def Logout(request):
	
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return JsonResponse({'status': 'failed', 'message': 'User not logged in!'})

		logout(request)
		return JsonResponse({'status': 'success', 'message': 'User logged out successfully!'})			


@csrf_exempt
def Delete(request):

	if request.method == 'POST':

		username = request.POST.get('username')
		if not PlayerInfo.objects.filter(username=username).exists():
			return JsonResponse({'status': 'failed', 'message': 'User not found!'})

		user = PlayerInfo.objects.get(username=username)
		user.delete()
		return JsonResponse({'status': 'success', 'message': 'User deleted successfully!'})