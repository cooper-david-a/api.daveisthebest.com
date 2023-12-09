from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="HIIT_creator"
    )

    def __str__(self):
        return self.user.username


class Schedule(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="schedules", null=True, blank=True
    )
    title = models.CharField(max_length=255)
    warmup = models.PositiveSmallIntegerField()
    cooldown = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Row(models.Model):
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="rows"
    )
    hard = models.PositiveSmallIntegerField()
    easy = models.PositiveSmallIntegerField()
    rounds = models.PositiveSmallIntegerField()
