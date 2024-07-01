from django import forms

from .models import Team, Player

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        labels = {'name': 'Название'}
             