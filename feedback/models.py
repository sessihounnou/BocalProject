from django.db import models
from django.db.models import Count

class Feedback(models.Model):
    EMOJI_CHOICES = (
        ('very bad', -2),
        ('bad', -1),
        ('happy', 1),
        ('very happy', 2),
    )
    emoji = models.CharField(max_length=10, choices=EMOJI_CHOICES, default='happy') 
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
