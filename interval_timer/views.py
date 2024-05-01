from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Schedule
from .serializers import ScheduleSerializer

MAX_SCHEDULES_PER_CREATOR = 10


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(schedule_creator__user = self.request.user).all()


    def update(self, request, *args, **kwargs):
        schedule = Schedule.objects.get(id=kwargs["pk"])
        if (
            request.user.id == schedule.schedule_creator.user.id
        ) or request.user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"error": "Only schedule creators or admin may update schedules"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def create(self, request, *args, **kwargs):
        creators_schedule_count = Schedule.objects.filter(schedule_creator__user_id = request.user).count()
        if creators_schedule_count < MAX_SCHEDULES_PER_CREATOR:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"error": "Maximum limit of saved schedules reached."},
                status=status.HTTP_403_FORBIDDEN,
            )


    def destroy(self, request, *args, **kwargs):
        schedule = Schedule.objects.get(id=kwargs["pk"])
        if (
            request.user.id == schedule.schedule_creator.user.id
        ) or request.user.is_staff:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"error": "Only schedule creators or admin may delete schedules"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
