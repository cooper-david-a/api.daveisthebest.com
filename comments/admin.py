from django.contrib import admin
from .models import Comment, Commenter

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'ok_to_display', 'date_entered', 'commenter', 'comment_text', 'parent_comment_id',
    'auto_is_spam','manual_is_spam','auto_positivity_rating', 'manual_positivity_rating']
    list_editable = ['ok_to_display', 'manual_is_spam', 'manual_positivity_rating']
    list_per_page = 25

@admin.register(Commenter)
class CommenterAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_per_page = 10

