# Generated by Django 4.1 on 2022-09-03 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="calendarprofile", options={"verbose_name": "Users Calendar Settings"},
        ),
        migrations.AddField(
            model_name="calendarprofile",
            name="shared_calendars",
            field=models.TextField(blank=True, null=True),
        ),
    ]
