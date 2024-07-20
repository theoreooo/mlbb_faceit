from celery import shared_task
from .matchmaking import matchmaking_process

@shared_task
def run_matchmaking():
    matchmaking_process()
