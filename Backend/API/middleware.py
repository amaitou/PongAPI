# middleware.py
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin
from .models import PlayerInfo
from django.conf import settings
import time

class RefreshTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get(settings.ACCESS_TOKEN)
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN)
        
        if access_token:
            try:
                token = AccessToken(access_token)
                
                expiry_time = token['exp']
                remaining_time = expiry_time - time.time()
                
                if remaining_time < 1 * 60:
                    
                    refresh = RefreshToken(refresh_token)
                    refresh.blacklist()
                    print('blacklisted')

                    try:
                        user = PlayerInfo.objects.get(id=token['user_id'])
                    except PlayerInfo.DoesNotExist:
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