from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .serializers import CoinFlipSerializer, CoinFlipStatsSerializer
from .models import CoinFlip, CoinFlipStats
from .filters import CoinFlipFilter



# Create your views here.

class CoinFlipperViewSet(ModelViewSet):
    """
    Coin flip results captured by the Goodthink Labs coin flipper.

    Each record contains the flip result (H/T/(U)nknown) and an optional image.
    Use /stats/ for aggregate statistics and /bulk/ for batch creation.

    Filters:
      ?flipped_after=DATETIME  Flips at or after this datetime
      ?flipped_before=DATETIME Flips at or before this datetime
      ?flipped_date=DATE       Flips on a specific date (YYYY-MM-DD)

    Ordering:
      ?ordering=id|flipped_at|recorded_at (prefix with - for descending)
    """
    queryset = CoinFlip.objects.all()
    serializer_class = CoinFlipSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filterset_class = CoinFlipFilter
    ordering_fields = ['id','flipped_at','recorded_at']
    ordering = ['-id']


    def perform_create(self, serializer):
        image = self.request.FILES.get('image')
        instance = serializer.save(image=None)
        if image:
            instance.image = image
            instance.save(update_fields=['image'])
        self._update_stats(instance.result)

    def _update_stats(self, result):
        with transaction.atomic():
            stats = CoinFlipStats.objects.select_for_update().get(pk=1)
            stats.total += 1

            if result == 'H':
                stats.heads += 1
            elif result == 'T':
                stats.tails += 1
            else:
                stats.unknown += 1

            if result != 'U':
                if result == stats.current_run_result:
                    stats.current_run_length += 1
                else:
                    stats.current_run_result = result
                    stats.current_run_length = 1

                if result == 'H':
                    stats.longest_run_heads = max(
                        stats.longest_run_heads, stats.current_run_length)
                elif result == 'T':
                    stats.longest_run_tails = max(
                        stats.longest_run_tails, stats.current_run_length)

            stats.save()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = CoinFlipStats.get()
        serializer = CoinFlipStatsSerializer(stats)
        return Response(serializer.data)


    @action(detail=True, methods=['post'])
    def image(self, request, pk=None):
        flip = self.get_object()
        flip.image = request.FILES.get('image')
        flip.save()
        return Response({'status': 'image saved'}, status=200)
    
    @action(detail=False, methods=['get'])
    def results(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        results = queryset.values_list('result', flat=True)
        return Response(list(results))

class CoinFlipperBulkView(APIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def post(self, request):
        serializer = CoinFlipSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

