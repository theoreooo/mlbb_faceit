from django.contrib.auth.models import AbstractUser
from django.db import models

class Team(models.Model):
    "Команда"
    name = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Player(AbstractUser):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    game_account_id = models.IntegerField(unique=True, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return self.username

class PlayerStats(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='stats')
    elo = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    winstreak = models.IntegerField(default=0)

    @property
    def winrate(self):
        if self.matches > 0:
            return round((self.wins / self.matches) * 100, 2)
        return 0.0
    
    def __str__(self):
        return f'Stats for {self.player.username}'