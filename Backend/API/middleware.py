
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

        if not current_access_token:
            return None
        
        try:
            AccessToken(current_access_token)
            return None
        except TokenError:
            pass

        current_refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN)

        print("- current_refresh_token: ", current_refresh_token)
        print("- current_access_token: ", current_access_token)

        if not current_refresh_token:
            return None
            
        try:
            decoded_refresh_token = RefreshToken(current_refresh_token)
        except TokenError:
            response = self.get_response(request)
            response.delete_cookie(settings.ACCESS_TOKEN)
            response.delete_cookie(settings.REFRESH_TOKEN)
            return response
        
        user_id = decoded_refresh_token["user_id"]

        try:
            user = UserInfo.objects.get(id=user_id)
        except UserInfo.DoesNotExist:
            response = self.get_response(request)
            response.delete_cookie(settings.ACCESS_TOKEN)
            response.delete_cookie("refresh_token")
            return response
    
        new_created_access_token = str(decoded_refresh_token.access_token)

        print("- refresh_toke: ", str(decoded_refresh_token))
        print("- new_created_access_token: ", new_created_access_token)
        request.COOKIES[settings.ACCESS_TOKEN] = new_created_access_token

        response = self.get_response(request)

        response.set_cookie(settings.ACCESS_TOKEN, new_created_access_token, httponly=False)

        return response
