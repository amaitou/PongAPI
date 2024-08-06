
from .models import PlayerInfo
from rest_framework import serializers

class PlayerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerInfo
        fields = '__all__'