from django.db import models
from django.conf import settings
import random

# Create your models here.

class MatchmakingQueue(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    elo = models.IntegerField()
    join_time = models.DateTimeField(auto_now_add=True)
    matched = models.BooleanField(default=False)
    search_start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.player.username} - {self.elo}'

class Match(models.Model):
    team1 = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team1')
    team2 = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team2')
    created_at = models.DateTimeField(auto_now_add=True)
    elo_difference = models.FloatField()
    captain_team1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='captain_team1', null=True, blank=True, on_delete=models.SET_NULL)
    captain_team2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='captain_team2', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Match {self.id} - Elo difference: {self.elo_difference}'

    def select_captains(self):
        team1_players = list(self.team1.all())
        team2_players = list(self.team2.all())
        if team1_players:
            self.captain_team1 = random.choice(team1_players)
        if team2_players:
            self.captain_team2 = random.choice(team2_players)
        self.save()