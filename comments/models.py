from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Commenter(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commenter"
    )

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )
    date_entered = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(
        Commenter,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    comment_text = models.CharField(max_length=255)
    manual_positivity_rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True
    )
    auto_positivity_rating = models.SmallIntegerField(null=True, blank=True)
    ok_to_display = models.BooleanField(default=True)
    auto_is_spam = models.BooleanField(default=False)
    manual_is_spam = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_entered"]

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
