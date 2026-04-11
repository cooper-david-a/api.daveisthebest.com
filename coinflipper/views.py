from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CoinFlipSerializer
from .models import CoinFlip



# Create your views here.

class CoinFlipperViewSet(ModelViewSet):
    queryset = CoinFlip.objects.all()
    serializer_class = CoinFlipSerializer

    @action(detail=True, methods=['post'])
    def image(self, request, pk=None):
        flip = self.get_object()
        flip.image = request.FILES.get('image')
        flip.save()
        return Response({'status': 'image saved'}, status=200)

class CoinFlipperBulkView(APIView):
    def post(self, request):
        serializer = CoinFlipSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

