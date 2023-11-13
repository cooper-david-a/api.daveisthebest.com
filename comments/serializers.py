from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "ok_to_display",
            "date_entered",
            "commenter_name",
            "comment_text",
            "parent_comment",
            "replies"
        ]

