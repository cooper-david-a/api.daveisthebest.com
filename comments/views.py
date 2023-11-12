from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer

class CommentsViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(ok_to_display=True).select_related('parent_comment').all()

