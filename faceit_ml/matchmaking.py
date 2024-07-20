# matchmaking.py

from datetime import timedelta
from itertools import combinations
from django.utils import timezone
from .models import MatchmakingQueue, Match
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def calculate_team_elo_difference(team1, team2):
    avg_elo_team1 = sum(player.elo for player in team1) / len(team1)
    avg_elo_team2 = sum(player.elo for player in team2) / len(team2)
    return abs(avg_elo_team1 - avg_elo_team2)

def calculate_max_min_elo_difference_between_teams(team1, team2):
    all_elos = [player.elo for player in team1] + [player.elo for player in team2]
    return max(all_elos) - min(all_elos)

def matchmaking_process():
    players = list(MatchmakingQueue.objects.filter(matched=False).order_by('join_time'))

    for player in players:
        if player.search_start_time is None:
            player.search_start_time = timezone.now()
            player.save()

    match = find_best_match(players)
    if match:
        team1, team2, difference = match
        match_instance = Match.objects.create(elo_difference=difference)
        match_instance.team1.set([player.player for player in team1])
        match_instance.team2.set([player.player for player in team2])
        match_instance.select_captains()

        MatchmakingQueue.objects.filter(player__in=[p.player for p in team1] + [p.player for p in team2]).update(matched=True)
        
        # Отправка уведомлений
        channel_layer = get_channel_layer()
        for player in [p.player for p in team1] + [p.player for p in team2]:
            async_to_sync(channel_layer.group_send)(
                f"matchmaking_{player.id}",
                {
                    'type': 'match_found',
                    'message': f"Match found! You have 30 seconds to accept."
                }
            )
    else:
        print("No suitable match found")

def find_best_match(players):
    best_match = None
    best_difference = float('inf')

    now = timezone.now()

    for team1 in combinations(players, 5):
        remaining_players = set(players) - set(team1)
        for team2 in combinations(remaining_players, 5):
            team1_elo = [player.elo for player in team1]
            team2_elo = [player.elo for player in team2]

            max_elo = max(team1_elo + team2_elo)
            min_elo = min(team1_elo + team2_elo)
            max_min_diff = max_elo - min_elo

            elo_difference_limit = 700 if any(player.search_start_time and (now - player.search_start_time) > timedelta(minutes=1) for player in team1 + team2) else 500

            if max_min_diff <= elo_difference_limit:
                inter_team_difference = calculate_team_elo_difference(team1, team2)
                
                if inter_team_difference < best_difference:
                    best_difference = inter_team_difference
                    best_match = (team1, team2, inter_team_difference)
    
    return best_match
