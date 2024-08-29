from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('callback', Authentication42.as_view(), name='callback'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefresher.as_view(), name='refresh'),
    path('users/', AllUsersView.as_view(), name='token'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path("update_password/", UpdatePasswordView.as_view(), name="password_update"),
    path("settings/", SettingsView.as_view(), name="profile_update"),
    path("email_verification/", VerifyEmailView.as_view(), name="email_verification"),
    path("reset_password/", ResetPasswordView.as_view(), name="password_reset"),
    path("password_verification/", VerifyPasswordView.as_view(), name="password_verification"),
]