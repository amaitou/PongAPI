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
        
        current_access_token = request.COOKIES.get(settings.ACCESS_TOKEN)

        if current_access_token:
            try:
                AccessToken(current_access_token)
                return None
            except TokenError:
                pass
        
        current_refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN)

        if current_refresh_token:

            try:
                
                decoded_refresh_token = RefreshToken(current_refresh_token)
            
            except TokenError:

                response = self.get_response(request)
                response.delete_cookie(settings.ACCESS_TOKEN)
                response.delete_cookie(settings.REFRESH_TOKEN)

                return response

            user_id = decoded_refresh_token['user_id']

            decoded_refresh_token.blacklist()

            user = UserInfo.objects.get(id=user_id)

            new_token = RefreshToken.for_user(user)
            new_access_token = str(new_token.access_token)
            new_refresh_token = new_token

            request.COOKIES[settings.ACCESS_TOKEN] = new_access_token
            request.COOKIES[settings.REFRESH_TOKEN] = new_refresh_token

            response = self.get_response(request)

            response.set_cookie(settings.ACCESS_TOKEN, new_access_token)
            response.set_cookie(settings.REFRESH_TOKEN, new_refresh_token, httponly=True)

            return response

        else:
            return self.get_response(request)