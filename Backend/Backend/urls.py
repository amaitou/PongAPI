
from django.contrib import admin
from django.urls import path, include
from API.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('API.urls')),
    path('register/', include('API.urls')),
]
