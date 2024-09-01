from django.db import transaction
from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "created_at",
            "name",
            "email",
            "message",
        ]