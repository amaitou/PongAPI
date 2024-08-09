
from .models import PlayerInfo
from rest_framework import serializers

class PlayerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerInfo
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
    
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
