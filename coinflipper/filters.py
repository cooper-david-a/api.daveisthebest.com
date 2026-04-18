# filters.py
import django_filters
from .models import CoinFlip

class CoinFlipFilter(django_filters.FilterSet):
    flipped_after = django_filters.DateTimeFilter(field_name='flipped_at', lookup_expr='gte')
    flipped_before = django_filters.DateTimeFilter(field_name='flipped_at', lookup_expr='lte')
    flipped_date = django_filters.DateFilter(field_name='flipped_at', lookup_expr='date')

    class Meta:
        model = CoinFlip
        fields = ['flipped_after', 'flipped_before', 'flipped_date']