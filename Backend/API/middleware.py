# middleware.py
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin
from .models import UserInfo
from django.conf import settings
import time

class RefreshTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get(settings.ACCESS_TOKEN)
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN)
        
        if access_token and refresh_token:
            try:
                access = AccessToken(access_token)
                
                expired_time = access['exp']
                remaining_time = expired_time - time.time()
                
                if remaining_time < 60 * 60:
                    
                    refresh = RefreshToken(refresh_token)
                    refresh.blacklist()

                    try:
                        user = UserInfo.objects.get(id=access['user_id'])
                    except UserInfo.DoesNotExist:
                        return self.get_response(request)
                    refresh = RefreshToken.for_user(user)
                    new_access_token = str(refresh.access_token)
                    new_refresh_token = str(refresh)
                    
                    response = self.get_response(request)
                    response.set_cookie(settings.ACCESS_TOKEN, new_access_token, httponly=True)
                    response.set_cookie(settings.REFRESH_TOKEN, new_refresh_token, httponly=True)
                    
                    return response
            except TokenError:
                pass
        return self.get_response(request)