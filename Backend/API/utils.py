
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from .models import UserInfo

class Utils:

    @staticmethod
    def send_verification_email(data):
        email = EmailMessage(subject=data['subject'], body=data['body'], to=[data['email']])
        email.send()
    
    @staticmethod
    def create_jwt_for_user(user) -> dict:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        jwt = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return jwt
    
    @staticmethod
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
    
    @staticmethod
    def password_validation(password):

        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in password):
            errors.append('Password must contain at least one digit')
        if not any(char.isupper() for char in password):
            errors.append('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            errors.append('Password must contain at least one lowercase letter')
        if not any(char in '!@#$%^&*()_+' for char in password):
            errors.append('Password must contain at least one special character')
        
        if errors:
            raise ValidationError(errors)