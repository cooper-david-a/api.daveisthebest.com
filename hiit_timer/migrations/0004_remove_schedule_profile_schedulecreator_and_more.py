# Generated by Django 5.0 on 2023-12-19 23:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiit_timer', '0003_row_easy_description_row_hard_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='profile',
        ),
        migrations.CreateModel(
            name='ScheduleCreator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='hiit_timer.schedulecreator'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
