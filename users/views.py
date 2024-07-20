from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .models import Player, Team
from .forms import PlayerRegisterForm, TeamForm

# Create your views here.
def profile(request, username):
    player = get_object_or_404(Player, username=username)
    return render(request, 'users/profile.html', {'player': player})

def register(request):
    if  request.method != 'POST':
        form = PlayerRegisterForm()
    else:
        form = PlayerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('faceit_ml:index')
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def teams(request):
    teams = Team.objects.order_by('date_added')
    context = {'teams': teams}
    return render(request, 'users/teams.html', context)

def team(request, team_id):
    team = Team.objects.get(id=team_id)
    players = team.player_set.order_by('-date_added')
    context = {'team': team, 'players': players}
    return render(request, 'users/team.html', context)

def new_team(request):
    if request.method !='POST':
        form = TeamForm
    else:
        form = TeamForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:teams')
    
    context = {'form': form}
    return render(request, 'users/new_team.html', context)