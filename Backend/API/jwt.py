
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import UserInfo


def create_jwt_for_user(user) -> dict:
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    jwt = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return jwt

def get_user_from_jwt(token, __type) -> UserInfo:

    if __type == 'refresh':
        try:
            refresh_token = RefreshToken(token)
            user_id = refresh_token['user_id']
            try:
                user = UserInfo.objects.get(id=user_id)
                return user
            except UserInfo.DoesNotExist:
                return None
        except Exception as e:
            return None
    else:
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            try:
                user = UserInfo.objects.get(id=user_id)
                return user
            except UserInfo.DoesNotExist:
                return None
        except Exception as e:
            return None