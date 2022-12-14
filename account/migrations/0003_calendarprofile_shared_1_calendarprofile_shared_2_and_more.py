# Generated by Django 4.1 on 2022-09-06 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_alter_calendarprofile_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="calendarprofile",
            name="shared_1",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="calendarprofile",
            name="shared_2",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="calendarprofile",
            name="shared_3",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="calendarprofile",
            name="shared_4",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="calendarprofile",
            name="shared_calendars",
            field=models.TextField(
                blank=True,
                help_text="sandbox version, test this for json data.",
                null=True,
            ),
        ),
    ]
