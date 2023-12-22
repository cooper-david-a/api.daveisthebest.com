from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS,
)
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

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
