import datetime
from django.db import models

class DailyCardSet(models.Model):
    date = models.DateField(unique=True)
    card_1 = models.CharField(max_length=100)
    card_2 = models.CharField(max_length=100)
    card_3 = models.CharField(max_length=100)
    horoscope_message = models.TextField()

    def __str__(self):
        return f"Cards for {self.date}"