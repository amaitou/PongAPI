
from .models import UserInfo, UserGameStats
from rest_framework import serializers
from .utils import password_validation
from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperuserCommand


class UserRegistrationSerializer(serializers.ModelSerializer):
	
	password = serializers.CharField(write_only=True, required=False, validators=[password_validation])
	re_password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = UserInfo
		fields = ['id',
				'username',
				're_password',
				'first_name',
				'last_name',
				'email',
				'date_joined',
				'password',
				'avatar',
				'gender',
				'is_verified',]


	def validate(self, data):

		if 'password' in data:
			if not 're_password' in data \
				or ('re_password' in data and data['password'] != data['re_password']):
				raise serializers.ValidationError({'password': 'Passwords do not match'})
		return data

	def create(self, validated_data):

		if 're_password' in validated_data:
			validated_data.pop('re_password')

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

class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserInfo
		fields = ['id',
				'gender',
				'username',
				'first_name',
				'last_name',
				'email',
				'date_joined',
				'avatar',]

class PasswordUpdateSerializer(serializers.ModelSerializer):
	
	old_password = serializers.CharField(write_only=True, required=True)
	new_password = serializers.CharField(write_only=True, required=True)
	re_new_password = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = UserInfo
		fields = ['old_password', 'new_password', 're_new_password']

	def validate(self, data):

		if data['new_password'] != data['re_new_password']:
			raise serializers.ValidationError({'new_password': 'Passwords do not match'})
		return data
	
	def validate_old_password(self, value):
		user = self.context['request'].user
		if not user.check_password(value):
			raise serializers.ValidationError('Old password is incorrect')
		return value

	def update(self, instance, validated_data):
		instance.set_password(validated_data['new_password'])
		instance.save()
		return instance