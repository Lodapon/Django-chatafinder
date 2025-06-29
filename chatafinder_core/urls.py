from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tarot_chatbot.urls')),     # homepage and tarot chatbot
    path('daily/', include('daily_cards.urls')),  # card of the day
]