from django.db import transaction
from rest_framework import serializers
from .models import Profile, Schedule, Row


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ["id", "user_id"]


class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ["id", "hard", "easy", "rounds"]


class ScheduleSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True)
    profile = serializers.StringRelatedField()

    def create(self, validated_data):
        with transaction.atomic():
            rows = validated_data.pop("rows")
            schedule = Schedule.objects.create(**validated_data)

            Row.objects.bulk_create(
                [
                    Row(
                        schedule=schedule,
                        hard=row["hard"],
                        easy=row["easy"],
                        rounds=row["rounds"],
                    )
                    for row in rows
                ]
            )

            return schedule

    class Meta:
        model = Schedule
        fields = [
            "id",
            "profile",
            "title",
            "warmup",
            "cooldown",
            "rows",
        ]
