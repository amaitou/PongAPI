from django.urls import path
from .views.auth_view import *
from .views.password_views import *
from .views.profile_views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('register/', RegisterView.as_view(), name='registration'),
    path('callback', Authentication42View.as_view(), name='42_authentication'),
    path('login/', LoginConfirmationView.as_view(), name='login'),
    path('2fa/', TwoFactorAuthenticationView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', AllUsersView.as_view(), name='all_users'),
    path('profile/', ProfileView.as_view(), name='profile_owner'),
    path('profile/<str:username>/', ProfileView.as_view(), name='user_profile'),
    path("password_u/", PasswordUpdateView.as_view(), name="password_update"),
    path("profile_u/", ProfileUpdateView.as_view(), name="profile_update"),
    path("email_v/", EmailVerifyView.as_view(), name="email_verification"),
    path("password_r/", PasswordResetView.as_view(), name="password_reset"),
    path("password_v/", PasswordVerify.as_view(), name="password_verification"),
    path("password_c/", PasswordConfirmationView.as_view(), name="password_confirmation"),
    path("friend_o/", FriendOperationsView.as_view(), name="friendship"),
    path("friend_l/", FriendListView.as_view(), name="friendship_list"),
    path("friend_r/", FriendRequestView.as_view(), name="friendship_request"),
    path("f_requests/", FriendRequestView.as_view(), name="friendship_requests"),
]