from django.shortcuts import render, redirect
from .models import Team
from .forms import TeamForm

# Create your views here.

def index(request):
    return render(request, 'faceit_ml/index.html')

def teams(request):
    teams = Team.objects.order_by('date_added')
    context = {'teams': teams}
    return render(request, 'faceit_ml/teams.html', context)

def team(request, team_id):
    team = Team.objects.get(id=team_id)
    players = team.player_set.order_by('-date_added')
    context = {'team': team, 'players': players}
    return render(request, 'faceit_ml/team.html', context)

def new_team(request):
    if request.method !='POST':
        form = TeamForm
    else:
        form = TeamForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('faceit_ml:teams')
    
    context = {'form': form}
    return render(request, 'faceit_ml/new_team.html', context)

