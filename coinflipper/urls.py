from rest_framework import routers
from .views import CoinFlipperViewSet, CoinFlipperBulkView
from django.urls import path


router = routers.DefaultRouter()
router.register("", CoinFlipperViewSet, basename="coinfliper")

urlpatterns = [
    path('bulk/', CoinFlipperBulkView.as_view()),
] + router.urls