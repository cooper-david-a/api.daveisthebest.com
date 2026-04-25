from django.db import transaction
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
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
    manual_corrections = serializers.SerializerMethodField()
    correction_rate = serializers.SerializerMethodField()
    last_corrected_id = serializers.SerializerMethodField()

    class Meta:
        model = CoinFlipStats
        fields = [
            'total', 'heads', 'tails', 'unknown',
            'pct_heads', 'pct_tails',
            'longest_run_heads', 'longest_run_tails',
            'manual_corrections', 'correction_rate', 'last_corrected_id',
        ]

    def get_pct_heads(self, obj):
        flips = obj.total - obj.unknown
        return round(obj.heads / flips * 100, 2) if flips else 0

    def get_pct_tails(self, obj):
        flips = obj.total - obj.unknown
        return round(obj.tails / flips * 100, 2) if flips else 0

    def _get_correction_logs(self):
        if not hasattr(self, '_correction_logs'):
            ct = ContentType.objects.get_for_model(CoinFlip)
            self._correction_logs = LogEntry.objects.filter(content_type=ct, action_flag=CHANGE)
        return self._correction_logs

    def get_manual_corrections(self, obj):
        return self._get_correction_logs().count()

    def get_correction_rate(self, obj):
        return round(self.get_manual_corrections(obj) / obj.total, 4) if obj.total else 0

    def get_last_corrected_id(self, obj):
        last = self._get_correction_logs().order_by('-object_id').values_list('object_id', flat=True).first()
        return int(last) if last else None