
from rest_framework_simplejwt.tokens import RefreshToken


def create_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    token = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return token

