from django.contrib.auth.forms import UserCreationForm 
from .models import Player, Team
from django import forms


class PlayerRegisterForm(UserCreationForm):
    class Meta:
        model = Player
        fields = ('username', 'first_name', 'last_name', 'email', 'game_account_id', 'date_of_birth', 'avatar', 'password1', 'password2')

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        labels = {'name': 'Название'}
             