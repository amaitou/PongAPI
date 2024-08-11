from django.urls import path
from .views import RegisterView, LoginView, GetUser, LogoutView, UpdateUser

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', GetUser.as_view(), name='User'),
    path('update/', UpdateUser.as_view(), name='update'),
]
