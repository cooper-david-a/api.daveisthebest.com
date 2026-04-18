from django.db import transaction
from rest_framework import serializers
from .models import CoinFlip, CoinFlipStats


class CoinFlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinFlip
        fields = [
            "id",
            "recorded_at",
            "flipped_at",
            "result",
            "image"
        ]

class CoinFlipStatsSerializer(serializers.ModelSerializer):
    pct_heads = serializers.SerializerMethodField()
    pct_tails = serializers.SerializerMethodField()

    class Meta:
        model = CoinFlipStats
        fields = [
            'total', 'heads', 'tails', 'unknown',
            'pct_heads', 'pct_tails',
            'longest_run_heads', 'longest_run_tails'
        ]

    def get_pct_heads(self, obj):
        flips = obj.total - obj.unknown
        return round(obj.heads / flips * 100, 2) if flips else 0

    def get_pct_tails(self, obj):
        flips = obj.total - obj.unknown
        return round(obj.tails / flips * 100, 2) if flips else 0