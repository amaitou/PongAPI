from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogoutView, UpdateUser, UserProfile, GetGameStats

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='User'),
    path('update/', UpdateUser.as_view(), name='update'),
    path('profile/<str:username>', UserProfile.as_view(), name='user_profile'),
    path('stats/', GetGameStats.as_view(), name='getuser'),
]