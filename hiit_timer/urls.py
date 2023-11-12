from django.urls import path
from rest_framework import routers
from .views import ScheduleViewSet, RowViewSet, ProfileViewSet


router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("schedules", ScheduleViewSet, basename="schedules")
router.register("rows", RowViewSet, basename="rows")

urlpatterns = router.urls
