
from rest_framework import serializers
from ..models import UserInfo
from ..utils import Utils

class RegistrationSerializer(serializers.ModelSerializer):
	
	password = serializers.CharField(write_only=True, required=False, validators=[Utils.password_validation])
	re_password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = UserInfo
		fields = ['id', 'username', 're_password', 'first_name', 'last_name', 'email', 'date_joined', 'password', 'avatar', 'gender', 'is_verified']

	def validate(self, data):

		if 'password' in data:
			if not 're_password' in data \
				or ('re_password' in data and data['password'] != data['re_password']):
				raise serializers.ValidationError({'password': 'Passwords do not match'})
		return data

	def create(self, validated_data):

		password_exists = 'password' in validated_data
		email_exists = 'email' in validated_data

		if 're_password' in validated_data:
			validated_data.pop('re_password')

		if not password_exists:
			user = UserInfo(**validated_data)
			user.save()
			return user
		
		if not 'avatar' in validated_data:
			if validated_data["gender"] == "M":
				validated_data["avatar"] = "/media/avatars/man.png"
			elif validated_data["gender"] == "f":
				validated_data["avatar"] = "/media/avatar/woman.png"
			else:
				validated_data["avatar"] = "/media/avatars/unknown.png"

		if password_exists:
			password = validated_data.pop('password')
		
		if "email" in validated_data:
			email = validated_data.pop('email')

		user = UserInfo(**validated_data)

		if password_exists:
			user.set_password(password)
		
		if email_exists:
			user.email = email.strip().lower()
		user.save()

		return user

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserInfo
		fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'avatar', 'gender']

class ProfileUpdateSerializer(serializers.ModelSerializer):
	
	email = serializers.EmailField(required=True)

	class Meta:
		model = UserInfo
		fields = ['first_name', 'last_name', 'email', 'gender', 'username', 'two_fa', 'avatar']

	def validate_email(self, value):
		user = self.context['request'].user
		if UserInfo.objects.exclude(pk=user.pk).filter(email=value).exists():
			raise serializers.ValidationError({"email": "This email is already in use."})
		return value
	
	
	def validate_username(self, value):
		user = self.context['request'].user
		if UserInfo.objects.exclude(pk=user.pk).filter(username=value).exists():
			raise serializers.ValidationError({"username": "This username is already in use."})
		return value

	def validate_two_fa(self, value):
		if not value in [True, False]:
			raise serializers.ValidationError({"two_fa": "Invalid value"})
		return value
	
	def update(self, instance, validated_data):

		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		instance.email = validated_data.get('email', instance.email)
		instance.username = validated_data.get('username', instance.username)
		instance.two_fa = validated_data.get('two_fa', instance.two_fa)

		instance.save()

		return instance