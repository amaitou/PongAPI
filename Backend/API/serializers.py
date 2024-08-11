
from .models import UserInfo
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'gender']
    
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        if email is not None:
            instance.email = email.lower()
        instance.save()
        return instance

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

class GetUseBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender']
    
    def get(self, instance):
        return instance