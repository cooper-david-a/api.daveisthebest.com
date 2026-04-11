from django.db import models
from django.utils import timezone

# Create your models here.

class CoinFlip(models.Model):
    result_choices = [("H", "Heads"),("T", "Tails"),("U", "Unknown")]

    recorded_at = models.DateTimeField(auto_now_add=True)
    flipped_at = models.DateTimeField(default=timezone.now)
    result = models.CharField(choices=result_choices, max_length=1, default="U")
    image = models.ImageField(upload_to='coinflipper/', blank=True, null=True)