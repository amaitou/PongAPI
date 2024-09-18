
from rest_framework import serializers
from ..models import UserGameStats

class GameStatsSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserGameStats
		fields = "__all__"