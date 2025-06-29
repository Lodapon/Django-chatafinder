from django.db import models

class TarotCard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image_filename = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name