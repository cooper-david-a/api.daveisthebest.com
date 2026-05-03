from django.contrib import admin
from django.utils.html import format_html
from .models import CoinFlip, ActiveCoin


@admin.register(ActiveCoin)
class ActiveCoinAdmin(admin.ModelAdmin):
    fields = ["number"]

    def has_add_permission(self, request):
        return not ActiveCoin.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CoinFlip)
class FlipAdmin(admin.ModelAdmin):
    list_display = ["id", "flipped_at", "recorded_at", "result", "coin", "checked", "image_preview"]
    list_filter = ["result", "checked", "coin", "flipped_at", "recorded_at"]
    list_editable = ["result"]
    readonly_fields = ["coin", "image_preview"]
    fields = ["result", "flipped_at", "image", "image_preview", "coin", "checked"]
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