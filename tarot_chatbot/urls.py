from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('tarot/', views.tarot_chat, name='tarot_chat'),
    path('select/', views.select_cards, name='select_cards'),
]