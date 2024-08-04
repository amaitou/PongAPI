
from django.db import models
from time import timezone

class PlayerBasicInfo(models.Model):

    player_username = models.CharField(max_length=30, unique = True, db_index = True)
    player_email = models.EmailField(max_length=125, unique = True, db_index = True)
    player_password = models.CharField(max_length=255)

    class Meta:
        
        db_table = 'PlayerBasicInfo'
        verbose_name = 'PlayerBasicInfo'
    
    def __str__(self) -> str:
        return f"{self.player_username}"

class PlayerDetailInfo(models.Model):

    PLAYER_GENDER = [
        ('M', 'M'),
        ('F', 'F'),
        ('N', 'N'),
    ]

    player_id = models.ForeignKey(PlayerBasicInfo, on_delete=models.CASCADE, null = False)
    player_first_name = models.CharField(max_length=30)
    player_last_name = models.CharField(max_length=30)
    player_starting_date = models.DateTimeField()
    player_avatar = models.ImageField(upload_to = 'avatars/', null = True)
    player_gender = models.CharField(max_length=2, choices = PLAYER_GENDER, null = False, default = 'N')

    class Meta:
        
        db_table = 'PlayerDetailInfo'
        verbose_name = 'PlayerDetailInfo'
    
    def __str__(self) -> str:
        return f"{self.player_id.player_username}"

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

    player_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False)
    player_won_games = models.IntegerField(default = 0, null = False)
    player_level = models.IntegerField(default = 0, null = False)
    player_rank = models.CharField(max_length = 20, choices = RANK_CHOICES, default = 'Beginner', null = False)
    player_lost_games = models.IntegerField(default = 0, null = False)
    player_draw_games = models.IntegerField(default = 0, null = False)
    player_won_tournaments = models.IntegerField(default = 0, null = False)
    player_total_tournaments = models.IntegerField(default = 0, null = False)
    player_experience_points = models.IntegerField(default = 0, null = False)

    class Meta:
        
        db_table = 'PlayerGameStats'
        verbose_name = 'PlayerGameStats'
    
    def __str__(self) -> str:
        return f"{self.player_id.player_username}"


class GameResults(models.Model):

    player_1_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'winner')
    player_2_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'loser')
    player_1_score = models.IntegerField(default = 0, null = False)
    player_2_score = models.IntegerField(default = 0, null = False)
    game_date = models.DateTimeField(auto_now_add = True)
    game_id = models.AutoField(primary_key = True)

    class Meta:
        
        db_table = 'GameResults'
        verbose_name = 'GameResults'
        indexes = [
            models.Index(fields = ['player_1_id', 'player_2_id'])
        ]
    
    def __str__(self) -> str:
        return f"{self.player_1_id.player_username}, {self.player_2_id.player_username}"

class FriendRequests(models.Model):

    REQUEST_STATUS = {
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    }

    sender_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'request_sender')
    receiver_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'request_receiver')
    friend_request_id = models.AutoField(primary_key = True)
    request_status = models.CharField(max_length = 20, choices = REQUEST_STATUS, default = 'Pending', null = False)
    request_date = models.DateTimeField(auto_now_add = True)

    class Meta:
            
            db_table = 'FriendRequests'
            verbose_name = 'FriendRequests'
            unique_together = ('sender_id', 'receiver_id')

            indexes = [
                models.Index(fields = ['sender_id', 'receiver_id'])
            ]
    
    def __str__(self) -> str:
        return f"{self.sender_id.player_username}, {self.receiver_id.player_username}"

class FriendshipList(models.Model):

    player_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'player')
    friend_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'friend')
    friendship_date = models.DateTimeField(auto_now_add = True)
    friendship_id = models.AutoField(primary_key = True)

    class Meta:
        
        db_table = 'FriendshipList'
        verbose_name = 'FriendshipList'
        unique_together = ('player_id', 'friend_id')

        unique_together = ('player_id', 'friend_id')
        indexes = [
            models.Index(fields = ['player_id', 'friend_id'])
        ]
    
    def __str__(self):
        return f"{self.player_id.player_username}, {self.friend_id.player_username}"

class BlockList(models.Model):

    player_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'blocker')
    blocked_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'blocked')
    block_id = models.AutoField(primary_key = True)
    time_of_block = models.DateTimeField(auto_now_add = True)

    class Meta:
        
        db_table = 'BlockList'
        verbose_name = 'BlockList'
        unique_together = ('player_id', 'blocked_id')

        indexes = [
            models.Index(fields = ['player_id', 'blocked_id'])
        ]
    
    def __str__(self) -> str:
        return f"b{self.player_id.player_username}, {self.blocked_id.player_username}"

class Chat(models.Model):

    CHAT_STATUS = [
        ('chatted', 'chatted'),
        ('not_chatted', 'not_chatted'),
    ]
    player_1_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'player_1_instance')
    player_2_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'player_2_instance')
    chat_status = models.CharField(max_length = 20, choices = CHAT_STATUS, default = 'not_chatted', null = False)
    chat_id = models.AutoField(primary_key = True)

    class Meta:
        
        db_table = 'Chat'
        verbose_name = 'Chat'
        unique_together = ('player_1_id', 'player_2_id')

        indexes = [
            models.Index(fields = ['player_1_id', 'player_2_id'])
        ]
    
    def __str__(self) -> str:
        return f"{self.player_1_id.player_username},{self.player_2_id.player_username}"
    
    def create_conversation(self, sender_id: int, receiver_id: int, message_content: str) -> 'Conversation':
        if self.chat_status == 'not_chatted':
            self.chat_status = 'chatted'
            self.save()
            return Conversation.objects.create(sender_id = sender_id, receiver_id = receiver_id, message_content = message_content)



class Conversation(models.Model):
    sender_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'message_sender')
    receiver_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'message_receiver')
    message_content = models.TextField(null = False)
    message_date = models.DateTimeField(auto_now_add = True)
    message_id = models.AutoField(primary_key = True)

    class Meta:
        
        db_table = 'Conversation'
        verbose_name = 'Conversation'
        indexes = [
            models.Index(fields = ['sender_id', 'receiver_id'])
        ]
    
    def __str__(self) -> str:
        return f"{self.sender_id.player_username}, {self.receiver_id.player_username}"

class Notification(models.Model):

    NOTIFICATION_TYPE = [
        ('Friend Request', 'Friend Request'),
        ('Game Request', 'Game Request'),
        ('Game Result', 'Game Result'),
        ('Chat', 'Chat'),
        ('Tournament', 'Tournament'),
    ]

    player_id = models.ForeignKey(PlayerBasicInfo, on_delete = models.CASCADE, null = False, related_name = 'player_notification')
    notification_type = models.CharField(max_length = 20, choices = NOTIFICATION_TYPE, null = False)
    notification_content = models.TextField(null = False)
    notification_date = models.DateTimeField(auto_now_add = True)
    notification_id = models.AutoField(primary_key = True)
    notification_is_read = models.BooleanField(default = False, null = False)

    class Meta:
        
        db_table = 'Notification'
        verbose_name = 'Notification'
    
    def __str__(self) -> str:
        return f"{self.player_id.player_username}"
