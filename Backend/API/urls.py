from django.urls import path
from .views import RegisterView, LoginView, GetPlayer, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('player/', GetPlayer.as_view(), name='player'),
]
