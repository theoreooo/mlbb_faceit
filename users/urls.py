from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('teams/', include([
        path('', views.teams, name='teams'),  # /teams/
        path('new/', views.new_team, name='new_team'),  # /teams/new/
        path('<int:team_id>/', views.team, name='team'),  # /teams/1/ (где 1 - team_id)
    ])),
    path('<str:username>/', views.profile, name='profile'),
]

