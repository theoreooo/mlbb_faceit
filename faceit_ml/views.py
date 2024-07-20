from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import MatchmakingQueue, Match
from users.models import PlayerStats
from django.http import JsonResponse

def index(request):
    return render(request, 'faceit_ml/index.html')

@login_required
def join_matchmaking_queue(request):
    player = request.user
    player_stats = PlayerStats.objects.get(player=player)

    queue_entry, created = MatchmakingQueue.objects.get_or_create(
        player=player,
        matched=False,
        defaults={'elo': player_stats.elo, 'search_start_time': timezone.now()}
    )

    if not created:
        queue_entry.search_start_time = timezone.now()
        queue_entry.save()

    return JsonResponse({'success': True, 'in_queue': not created})

    
@login_required
def matchmaking_view(request):
    return render(request, 'faceit_ml/matchmaking.html')

@login_required
def matchmaking_status(request):
    player = request.user
    try:
        queue_entry = MatchmakingQueue.objects.get(player=player, matched=False)
        in_queue = True
    except MatchmakingQueue.DoesNotExist:
        in_queue = False

    in_game = Match.objects.filter(team1=player).exists() or Match.objects.filter(team2=player).exists()

    return JsonResponse({'in_queue': in_queue, 'in_game': in_game})


@login_required
def match_results(request):
    player = request.user
    matches = Match.objects.filter(team1=player) | Match.objects.filter(team2=player)
    
    return render(request, 'faceit_ml/match_results.html', {'matches': matches})

@login_required
def cancel_matchmaking_queue(request):
    if request.method == 'POST':
        player = request.user
        try:
            queue_entry = MatchmakingQueue.objects.get(player=player, matched=False)
            queue_entry.delete()
            message = "You have left the queue"
        except MatchmakingQueue.DoesNotExist:
            message = "You are not in the queue"

        return JsonResponse({'message': message})
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)
