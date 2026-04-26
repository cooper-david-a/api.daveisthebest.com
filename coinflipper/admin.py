from django.contrib import admin
from django.utils.html import format_html
from .models import CoinFlip

@admin.register(CoinFlip)
class FlipAdmin(admin.ModelAdmin):
    list_display = ["id", "flipped_at", "recorded_at", "result", "checked", "image_preview"]
    list_filter = ["result", "checked", "flipped_at", "recorded_at"]
    list_editable = ["result"]
    readonly_fields = ["image_preview"]
    fields = ["result", "flipped_at", "image", "image_preview", "checked"]
    list_per_page = 200
    actions = ["mark_checked"]

    def mark_checked(self, request, queryset):
        queryset.update(checked=True)
    mark_checked.short_description = "Mark selected flips as checked"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image Preview"