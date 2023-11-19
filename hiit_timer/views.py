from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Profile, Schedule, Row
from .serializers import ScheduleSerializer, RowSerializer, ProfileSerializer

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

class ScheduleViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Schedule.objects.all()
        return Schedule.objects.filter(profile__user_id=self.request.user.id)


class RowViewSet(ModelViewSet):
    queryset = Row.objects.all()
    serializer_class = RowSerializer
    permission_classes = [IsAuthenticated]
