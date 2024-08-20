
from .utils import password_validation
from rest_framework import serializers
from .models import UserInfo, UserGameStats

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    password = serializers.CharField(write_only=True, required=False, validators=[password_validation])

    def create(self, validated_data):

        if 'password' not in validated_data:
            user = UserInfo(**validated_data)
            user.save()
            return user

        password = validated_data.pop('password')
        user = UserInfo(**validated_data)
        user.set_password(password)
        user.save()

        return user



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def put(self, instance, validated_data):
        
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

class GetUserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender']

class GetGameStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGameStats
        fields = "__all__"