from django.contrib import admin
from .models import Schedule, Profile, Row

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_per_page = 10


class RowInline(admin.TabularInline):
    model = Row
    extra = 0


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["id", "profile"]
    list_per_page = 10
    inlines = [RowInline]


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ["id", "hard", "easy", "rounds"]
    list_per_page = 25
