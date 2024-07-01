""""Определяет схемы URL для faceit_ml"""

from django.urls import path

from . import views

app_name = 'faceit_ml'
urlpatterns = [
    path('', views.index, name='index'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:team_id>/', views.team, name='team'),
    path('new_team/', views.new_team, name='new_team'),
]