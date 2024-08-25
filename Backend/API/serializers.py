
from .models import UserInfo, UserGameStats
from rest_framework import serializers
from .utils import password_validation

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id',
                'username',
                'first_name',
                'last_name',
                'email',
                'date_joined',
                'password',
                'avatar',
                'gender',]

    password = serializers.CharField(write_only=True, required=False, validators=[password_validation])

    def create(self, validated_data):

        if 'password' not in validated_data:
            user = UserInfo(**validated_data)
            user.save()
            return user

        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = UserInfo(**validated_data)
        user.set_password(password)
        user.email = email.strip().lower()
        user.save()

        return user

class GetUserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender']

class GetGameStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGameStats
        fields = "__all__"

class GetUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id',
                'username',
                'first_name',
                'last_name',
                'email',
                'date_joined',
                'avatar',
                'gender',]