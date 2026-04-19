from django.db import models
from django.utils import timezone

# Create your models here.

def _flip_image_path(instance, filename):
    name, _, ext = filename.rpartition(".")
    return f"coinflipper/{name}_{instance.id}.{ext}"


class CoinFlip(models.Model):
    result_choices = [("H", "Heads"),("T", "Tails"),("U", "Unknown")]

    recorded_at = models.DateTimeField(auto_now_add=True)
    flipped_at = models.DateTimeField(default=timezone.now)
    result = models.CharField(choices=result_choices, max_length=1, default="U")
    image = models.ImageField(upload_to=_flip_image_path, blank=True, null=True)

class CoinFlipStats(models.Model):
    total = models.IntegerField(default=0)
    heads = models.IntegerField(default=0)
    tails = models.IntegerField(default=0)
    unknown = models.IntegerField(default=0)
    longest_run_heads = models.IntegerField(default=0)
    longest_run_tails = models.IntegerField(default=0)
    current_run_result = models.CharField(max_length=1, default='U')
    current_run_length = models.IntegerField(default=0)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj