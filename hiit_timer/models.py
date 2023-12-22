from django.db import models
from django.conf import settings


class ScheduleCreator(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schedule_creator"
    )

    def __str__(self):
        return self.user.username


class Schedule(models.Model):
    schedule_creator = models.ForeignKey(
        ScheduleCreator,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    title = models.CharField(max_length=100)
    warmup = models.PositiveSmallIntegerField()
    warmup_description = models.CharField(max_length=100)
    cooldown = models.PositiveSmallIntegerField()
    cooldown_description = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Row(models.Model):
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="rows"
    )
    hard = models.PositiveSmallIntegerField()
    hard_description = models.CharField(max_length=100)
    easy = models.PositiveSmallIntegerField()
    easy_description = models.CharField(max_length=100)
    rounds = models.PositiveSmallIntegerField()
