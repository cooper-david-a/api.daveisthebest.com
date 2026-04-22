from django.contrib import admin
from django.utils.html import format_html
from .models import CoinFlip

@admin.register(CoinFlip)
class FlipAdmin(admin.ModelAdmin):
    list_display = ["id", "flipped_at", "result", "image_preview"]
    list_editable = ["result"]
    readonly_fields = ["image_preview"]
    fields = ["result", "flipped_at", "image", "image_preview"]
    list_per_page = 25

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image Preview"