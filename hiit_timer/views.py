from rest_framework.viewsets import ModelViewSet
from .models import Profile, Schedule, Row
from .serializers import ScheduleSerializer, RowSerializer, ProfileSerializer

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ScheduleViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return Schedule.objects.all()


class RowViewSet(ModelViewSet):
    queryset = Row.objects.all()
    serializer_class = RowSerializer
