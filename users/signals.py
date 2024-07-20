from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Player, PlayerStats

@receiver(post_save, sender=Player)
def create_player_stats(sender, instance, created, **kwargs):
    if created:
        PlayerStats.objects.create(player=instance)
