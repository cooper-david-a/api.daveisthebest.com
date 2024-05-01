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
            user_id = self.context["request"].user.id
            (schedule_creator, created) = ScheduleCreator.objects.get_or_create(
                user_id=user_id
            )
            schedule = Schedule.objects.create(
                schedule_creator=schedule_creator, **validated_data
            )

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

    def update(self, instance, validated_data):
        with transaction.atomic():
            new_rows_data = validated_data.pop("rows")
            old_rows = instance.rows.all()

            for i in range(len(old_rows)):
                if i < len(new_rows_data):
                    old_rows[i].hard = new_rows_data[i].get("hard", old_rows[i].hard)
                    old_rows[i].hard_description = new_rows_data[i].get(
                        "hard_description", old_rows[i].hard_description
                    )
                    old_rows[i].easy = new_rows_data[i].get("easy", old_rows[i].hard)
                    old_rows[i].easy_description = new_rows_data[i].get(
                        "easy_description", old_rows[i].easy_description
                    )
                    old_rows[i].rounds = new_rows_data[i].get("rounds", old_rows[i].rounds)
                    old_rows[i].save()
                else:
                    old_rows[i].delete()

            for i in range(len(old_rows),len(new_rows_data)):
                Row.objects.create(
                        schedule=instance,
                        hard=new_rows_data[i].get("hard"),
                        hard_description=new_rows_data[i].get("hard_description"),
                        easy=new_rows_data[i].get("easy"),
                        easy_description=new_rows_data[i].get("easy_description"),
                        rounds=new_rows_data[i].get("rounds"),
                )

            return super().update(instance, validated_data)

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
