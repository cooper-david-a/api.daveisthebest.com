# Generated by Django 4.2.7 on 2023-11-12 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import file_sharing.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SharedFile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_uploaded", models.DateTimeField(auto_now_add=True)),
                ("description", models.CharField(max_length=100)),
                (
                    "file",
                    models.FileField(
                        upload_to="file_sharing/",
                        validators=[file_sharing.validators.validate_file_size],
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="file_sharing.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AccessEmail",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email", models.EmailField(max_length=70)),
                (
                    "file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="access_emails",
                        to="file_sharing.sharedfile",
                    ),
                ),
            ],
        ),
    ]