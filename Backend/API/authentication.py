
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request

class HeaderTokenAuthentication(JWTAuthentication):

    def authenticate(self, request: Request):

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None


        try:
            prefix, access_token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None


        validated_token = self.get_validated_token(access_token)
        user = self.get_user(validated_token)

        if user is None:
            return None

        return user, validated_token

