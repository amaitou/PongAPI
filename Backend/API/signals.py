
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserInfo, UserGameStats

@receiver(post_save, sender = UserInfo)
def create_instance_game_stats(sender, instance, created, **kwargs):
    if created:
        UserGameStats.objects.create(user_id = instance)