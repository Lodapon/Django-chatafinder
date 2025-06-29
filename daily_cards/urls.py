# daily_cards/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cards_of_the_day, name='cards_of_the_day'),
]