""""Определяет схемы URL для faceit_ml"""

from django.urls import path

from . import views

app_name = 'faceit_ml'
urlpatterns = [
    path('', views.index, name='index'),
]