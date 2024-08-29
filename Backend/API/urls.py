from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='registration'),
    path('callback', Authentication42View.as_view(), name='42_authentication'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefresherView.as_view(), name='token_refresher'),
    path('users/', AllUsersView.as_view(), name='all_users'),
    path('profile/', ProfileView.as_view(), name='profile_owner'),
    path('profile/<str:username>/', ProfileView.as_view(), name='user_profile'),
    path("password_u/", PasswordUpdateView.as_view(), name="password_update"),
    path("profile_u/", ProfileUpdateView.as_view(), name="profile_update"),
    path("email_v/", EmailVerifyView.as_view(), name="email_verification"),
    path("password_r/", PasswordResetView.as_view(), name="password_reset"),
    path("password_v/", PasswordVerifyView.as_view(), name="password_verification"),
]