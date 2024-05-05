from rest_framework import serializers
from .models import Comment, Commenter



class CommenterSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Commenter
        fields = ["id", "user_id"]

class CommentSerializer(serializers.ModelSerializer):
    commenter = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "ok_to_display",
            "date_entered",
            "commenter",
            "comment_text",
            "parent_comment",
            "replies"
        ]

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "comment_text",
            "parent_comment",
        ]

    def create(self, validated_data):
        user_id = self.context["request"].user.id
        (commenter,created) = Commenter.objects.get_or_create(user_id=user_id)
        comment = Comment.objects.create(
            commenter=commenter, **validated_data
        )
        return comment

