from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('callback', Authentication42.as_view(), name='callback'),
    path('refresh/', TokenRefresher.as_view(), name='refresh'),
    path('users/', UsersView.as_view(), name='token'),
]