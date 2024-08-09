from django.db import models
from django.contrib.auth.models import AbstractUser
from time import timezone

class PlayerInfo(AbstractUser):

    PLAYER_GENDER = [
        ('M', 'M'),
        ('F', 'F'),
        ('N', 'N'),
    ]

    avatar = models.ImageField(upload_to = 'avatars/', null = True)
    gender = models.CharField(max_length=2, choices = PLAYER_GENDER, null = True, default = 'N')
    email = models.EmailField(unique = True, null = False)
    first_name = models.CharField(max_length = 30, null = False)
    last_name = models.CharField(max_length = 30, null = False)
    username = models.CharField(max_length = 30, unique = True, null = False)

    class Meta:
        
        db_table = 'PlayerInfo'
        verbose_name = 'PlayerInfo'
        verbose_name_plural = 'PlayerInfo'
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return f"{self.username}"

class PlayerGameStats(models.Model):

    RANK_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Amateur', 'Amateur'),
        ('Semi-Pro', 'Semi-Pro'),
        ('Pro', 'Pro'),
        ('World Class', 'World Class'),
        ('Legendary', 'Legendary'),
        ('Ultimate', 'Ultimate'),
    ]

    player_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'player_gme_stats')
    won_games = models.IntegerField(default = 0, null = False)
    level = models.IntegerField(default = 0, null = False)
    rank = models.CharField(max_length = 20, choices = RANK_CHOICES, default = 'Beginner', null = False)
    lost_games = models.IntegerField(default = 0, null = False)
    draw_games = models.IntegerField(default = 0, null = False)
    won_tournaments = models.IntegerField(default = 0, null = False)
    total_tournaments = models.IntegerField(default = 0, null = False)
    experience_points = models.IntegerField(default = 0, null = False)

    class Meta:
        
        db_table = 'PlayerGameStats'
        verbose_name = 'PlayerGameStats'
        verbose_name_plural = 'PlayerGameStats'
    
    def __str__(self) -> str:
        return f"{self.player_id.username}"


class GameResults(models.Model):

    player_1_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'winner')
    player_2_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'loser')
    player_1_score = models.IntegerField(default = 0, null = False)
    player_2_score = models.IntegerField(default = 0, null = False)
    game_date = models.DateTimeField(auto_now_add = True)
    game_id = models.AutoField(primary_key = True)

    class Meta:
        
        db_table = 'GameResults'
        verbose_name = 'GameResults'
        verbose_name_plural = 'GameResults'
        indexes = [
            models.Index(fields = ['player_1_id', 'player_2_id'])
        ]
    
    def __str__(self) -> str:
        return f"{self.player_1_id.username}, {self.player_2_id.username}"

class FriendRequests(models.Model):

    REQUEST_STATUS = {
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    }

    sender_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'request_sender')
    receiver_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'request_receiver')
    friend_request_id = models.AutoField(primary_key = True)
    request_status = models.CharField(max_length = 20, choices = REQUEST_STATUS, default = 'Pending', null = False)
    request_date = models.DateTimeField(auto_now_add = True)

    class Meta:
            
            db_table = 'FriendRequests'
            verbose_name = 'FriendRequests'
            verbose_name_plural = 'FriendRequests'
            unique_together = ('sender_id', 'receiver_id')

            indexes = [
                models.Index(fields = ['sender_id', 'receiver_id'])
            ]
    
    def __str__(self) -> str:
        return f"{self.sender_id.username}, {self.receiver_id.username}"

class FriendshipList(models.Model):

    player_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'player')
    friend_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'friend')
    friendship_date = models.DateTimeField(auto_now_add = True)
    friendship_id = models.AutoField(primary_key = True)

    class Meta:
        
        db_table = 'FriendshipList'
        verbose_name = 'FriendshipList'
        verbose_name_plural = 'FriendshipList'
        unique_together = ('player_id', 'friend_id')

        unique_together = ('player_id', 'friend_id')
        indexes = [
            models.Index(fields = ['player_id', 'friend_id'])
        ]
    
    def __str__(self):
        return f"{self.player_id.username}, {self.friend_id.username}"

class BlockList(models.Model):

    player_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'blocker')
    blocked_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'blocked')
    block_id = models.AutoField(primary_key = True)
    time_of_block = models.DateTimeField(auto_now_add = True)

    class Meta:
        
        db_table = 'BlockList'
        verbose_name = 'BlockList'
        verbose_name_plural = 'BlockList'
        unique_together = ('player_id', 'blocked_id')

        indexes = [
            models.Index(fields = ['player_id', 'blocked_id'])
        ]
    
    def __str__(self) -> str:
        return f"b{self.player_id.username}, {self.blocked_id.username}"

class Chat(models.Model):

    CHAT_STATUS = [
        ('chatted', 'chatted'),
        ('not_chatted', 'not_chatted'),
    ]
    player_1_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'player_1_instance')
    player_2_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'player_2_instance')
    chat_status = models.CharField(max_length = 20, choices = CHAT_STATUS, default = 'not_chatted', null = False)
    chat_id = models.AutoField(primary_key = True)

    class Meta:
        
        db_table = 'Chat'
        verbose_name = 'Chat'
        verbose_name_plural = 'Chat'
        unique_together = ('player_1_id', 'player_2_id')

        indexes = [
            models.Index(fields = ['player_1_id', 'player_2_id'])
        ]
    
    def __str__(self) -> str:
        return f"{self.player_1_id.username},{self.player_2_id.username}"
    
    def create_conversation(self, sender_id: int, receiver_id: int, message_content: str) -> 'Conversation':
        if self.chat_status == 'not_chatted':
            self.chat_status = 'chatted'
            self.save()
            return Conversation.objects.create(sender_id = sender_id, receiver_id = receiver_id, message_content = message_content)



class Conversation(models.Model):
    sender_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'message_sender')
    receiver_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'message_receiver')
    message_content = models.TextField(null = False)
    message_date = models.DateTimeField(auto_now_add = True)
    message_id = models.AutoField(primary_key = True)

    class Meta:
        
        db_table = 'Conversation'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversation'
        indexes = [
            models.Index(fields = ['sender_id', 'receiver_id'])
        ]
    
    def __str__(self) -> str:
        return f"{self.sender_id.username}, {self.receiver_id.username}"

class Notification(models.Model):

    NOTIFICATION_TYPE = [
        ('Friend Request', 'Friend Request'),
        ('Game Request', 'Game Request'),
        ('Game Result', 'Game Result'),
        ('Chat', 'Chat'),
        ('Tournament', 'Tournament'),
    ]

    player_id = models.ForeignKey(PlayerInfo, on_delete = models.CASCADE, null = False, related_name = 'player_notification')
    notification_type = models.CharField(max_length = 20, choices = NOTIFICATION_TYPE, null = False)
    notification_content = models.TextField(null = False)
    notification_date = models.DateTimeField(auto_now_add = True)
    notification_id = models.AutoField(primary_key = True)
    notification_is_read = models.BooleanField(default = False, null = False)

    class Meta:
        
        db_table = 'Notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notification'
    
    def __str__(self) -> str:
        return f"{self.player_id.username}"
