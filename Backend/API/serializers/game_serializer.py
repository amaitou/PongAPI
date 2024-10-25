
from rest_framework import serializers
from ..models import UserGameStats, GameResults

class GameStatsSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserGameStats
		fields = "__all__"

class GameResultRecordingSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = GameResults
		fields = "__all__"
	
	def validate(self, data):

		winner = data.get('player_1')
		loser = data.get('player_2')
		winner_score = data.get('score_1')
		loser_score = data.get('score_2')

		if winner == loser:
			raise serializers.ValidationError("Both players cannot be the same")

		if winner_score < 0 or loser_score < 0:
			raise serializers.ValidationError("Scores cannot be negative")
		
		if loser_score > winner_score:
			raise serializers.ValidationError("Loser score cannot be greater than winner score")

		return data
	
	def create(self, validated_data):
		winner = validated_data.get('player_1')
		loser = validated_data.get('player_2')
		winner_score = validated_data.get('score_1')
		loser_score = validated_data.get('score_2')

		is_draw = winner_score == loser_score
		
		game = GameResults.objects.create(player_1 = winner, player_2 = loser, score_1 = winner_score, score_2 = loser_score, is_draw = is_draw)
		game.save()
		return game