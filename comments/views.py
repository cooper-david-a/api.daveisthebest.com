from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import Comment
from .serializers import CommentSerializer


class CommentsViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    serializer_class = CommentSerializer
    ok_replies_queryset = Comment.objects.filter(ok_to_display=True)
    permission_classes = [AllowAny]
    queryset = (
        Comment.objects.filter(ok_to_display=True)
        .prefetch_related(Prefetch("replies", queryset=ok_replies_queryset))
        .select_related("parent_comment")
    )