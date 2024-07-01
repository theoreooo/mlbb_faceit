from django.db import models
from django.conf import settings

# Create your models here.

class Team(models.Model):
    "Команда"
    name = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    nickname = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nickname}"
