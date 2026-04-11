from django.db import transaction
from rest_framework import serializers
from .models import CoinFlip


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