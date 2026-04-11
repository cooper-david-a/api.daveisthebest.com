from django.contrib import admin
from .models import CoinFlip

# Register your models here.

@admin.register(CoinFlip)
class FlipAdmin(admin.ModelAdmin):
    list_display = ["id", "flipped_at", "result", "image"]
    list_per_page = 25