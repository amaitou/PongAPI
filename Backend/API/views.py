from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import *

def Index(request):
	return render(request, 'API/index.html', {})

@csrf_exempt
def Register(request):
	if request.method == "POST":
		check_user = PlayerBasicInfo.objects
		if check_user.filter(player_username = request.POST.get("username")).exists()  or check_user.filter(player_email = request.POST.get("email")).exists():
			return JsonResponse({"message": "User Already Exists"})
		created_user = check_user.create(
			player_username = request.POST.get("username"),
			player_email = request.POST.get("email"),
			player_password = make_password(request.POST.get("password")))
		created_user.save()
		return JsonResponse({"message": "User Created Successfully"})
	else:
		print("request.GET")
		return render(request, 'API/register.html', {})


@csrf_exempt
def Login(request):
	if request.method == "POST":
		check_user = PlayerBasicInfo.objects
		if check_user.filter(player_username = request.POST.get("username")).exists():
			user = check_user.get(player_username = request.POST.get("username"))
			if check_password(request.POST.get("password"), user.player_password):
				return JsonResponse({"message": "Login Successful"})
			else:
				return JsonResponse({"message": "Invalid Password"})
		else:
			return JsonResponse({"message": "User Not Found"})
	else:
		return render(request, 'API/login.html', {})