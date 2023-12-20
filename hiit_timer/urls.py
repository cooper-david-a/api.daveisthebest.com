from django.urls import path
from rest_framework import routers
from .views import ScheduleViewSet, RowViewSet, ScheduleCreatorViewSet


router = routers.DefaultRouter()
router.register("schedule-creators", ScheduleCreatorViewSet, basename="schedule_creators")
router.register("schedules", ScheduleViewSet, basename="schedules")
router.register("rows", RowViewSet, basename="rows")

urlpatterns = router.urls
