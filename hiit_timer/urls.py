from django.urls import path
from rest_framework import routers
from .views import ScheduleViewSet


router = routers.DefaultRouter()
router.register("schedules", ScheduleViewSet, basename="schedules")

urlpatterns = router.urls
