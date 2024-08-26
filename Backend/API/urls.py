from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('callback', Authentication42.as_view(), name='callback'),
    path('refresh/', TokenRefresher.as_view(), name='refresh'),
    path('users/', AllUsersView.as_view(), name='token'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path("update_password/", UpdatePasswordView.as_view(), name="password_reset"),
    path("email_verification/", VerifyEmailView.as_view(), name="email_verification"),
]