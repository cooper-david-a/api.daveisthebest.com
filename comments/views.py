from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment
from .serializers import CommentSerializer, PostCommentSerializer


class CommentsViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    ok_replies_queryset = Comment.objects.filter(ok_to_display=True)
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = (
        Comment.objects.filter(ok_to_display=True)
        .prefetch_related(Prefetch("replies", queryset=ok_replies_queryset))
        .select_related("parent_comment")
    )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCommentSerializer
        return CommentSerializer