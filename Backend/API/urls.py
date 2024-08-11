from django.urls import path
from .views import RegisterView, LoginView, GetMe, LogoutView, UpdateUser, GetUser, GetGameStats

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', GetMe.as_view(), name='User'),
    path('update/', UpdateUser.as_view(), name='update'),
    path('get_user/<str:username>', GetUser.as_view(), name='getuser'),
    path('get_game_stats/', GetGameStats.as_view(), name='getuser'),
]