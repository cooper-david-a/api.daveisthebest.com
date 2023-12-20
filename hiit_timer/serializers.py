from django.db import transaction
from rest_framework import serializers
from .models import ScheduleCreator, Schedule, Row


class ScheduleCreatorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = ScheduleCreator
        fields = ["id", "user_id"]


class RowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = [
            "id",
            "hard_description",
            "hard",
            "easy_description",
            "easy",
            "rounds",
        ]


class ScheduleSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True)
    schedule_creator = serializers.StringRelatedField()

    def create(self, validated_data):
        with transaction.atomic():
            rows = validated_data.pop("rows")
            schedule = Schedule.objects.create(**validated_data)

            Row.objects.bulk_create(
                [
                    Row(
                        schedule=schedule,
                        hard=row["hard"],
                        hard_description=row["hard_description"],
                        easy=row["easy"],
                        easy_description=row["easy_description"],
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
            "schedule_creator",
            "title",
            "warmup_description",
            "warmup",
            "cooldown_description",
            "cooldown",
            "rows",
        ]
