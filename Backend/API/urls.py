from django.urls import path
from .views.auth_view import *
from .views.password_views import *
from .views.profile_views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('callback', Authentication42View.as_view(), name='42_authentication'),
    path('login/', LoginConfirmationView.as_view(), name='login'),
    path('2fa/', TwoFactorAuthenticationView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', GetAllUsersView.as_view(), name='all_users'),
    path('profile/', GetProfileView.as_view(), name='profile_owner'),
    path('profile/<str:username>/', GetProfileView.as_view(), name='user_profile'),
    path("password_u/", PasswordUpdatingView.as_view(), name="password_update"),
    path("profile_u/", ProfileUpdatingView.as_view(), name="profile_update"),
    path("email_v/", EmailVerificationView.as_view(), name="email_verification"),
    path("password_r/", PasswordResettingView.as_view(), name="password_reset"),
    path("password_v/", PasswordVerificationView.as_view(), name="password_verification"),
    path("password_c/", PasswordConfirmationView.as_view(), name="password_confirmation"),
    path("friend_o/", FriendOperationsView.as_view(), name="friendship"),
    path("friend_l/", FriendshipListView.as_view(), name="friendship_list"),
    path("friend_r/", FriendRequestsView.as_view(), name="friendship_request"),
]