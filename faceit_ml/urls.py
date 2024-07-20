""""Определяет схемы URL для faceit_ml"""

from django.urls import path

from . import views

app_name = 'faceit_ml'
urlpatterns = [
    path('', views.index, name='index'),
    path('join_queue/', views.join_matchmaking_queue, name='join_queue'),
    path('status/', views.matchmaking_status, name='matchmaking_status'),
    path('cancel_queue/', views.cancel_matchmaking_queue, name='cancel_queue'),
    path('results/', views.match_results, name='match_results'),
    path('matchmaking/', views.matchmaking_view, name='matchmaking_view'),
]