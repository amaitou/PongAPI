

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from django.conf import settings

class HeaderTokenAuthentication(JWTAuthentication):

    def authenticate(self, request: Request):
        # Skip authentication for specific paths if needed
        if request.path == '/api/register/':
            return None

        # Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        # Expecting the header in the format: "Bearer <token>"
        try:
            prefix, access_token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None

        # Validate the token
        validated_token = self.get_validated_token(access_token)
        user = self.get_user(validated_token)

        if user is None:
            return None

        return user, validated_token

