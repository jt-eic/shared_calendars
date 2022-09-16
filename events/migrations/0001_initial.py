# Generated by Django 4.1 on 2022-09-01 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AllEvents",
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
                ("cal_id", models.CharField(max_length=150)),
                ("start", models.CharField(max_length=60)),
                ("end", models.CharField(max_length=60)),
                ("summary", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=100)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Calendar Event",
                "verbose_name_plural": "Calendar Events",
            },
        ),
    ]
