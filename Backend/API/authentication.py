
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .models import PlayerInfo

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        return token

class CookieTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Retrieve the access token from the cookies
        token = request.COOKIES.get('access')
        if not token:
            return None  # No token found, proceed with login

        try:
            # Validate the access token
            validated_token = AccessToken(token)
            user = User.objects.get(id=validated_token['user_id'])  # Replace with your user model if different
        except Exception as e:
            return None  # Token is invalid or expired

        return (user, None)