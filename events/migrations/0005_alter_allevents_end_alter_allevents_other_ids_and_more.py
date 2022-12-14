# Generated by Django 4.1 on 2022-09-16 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_allevents_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="allevents", name="end", field=models.CharField(max_length=90),
        ),
        migrations.AlterField(
            model_name="allevents",
            name="other_ids",
            field=models.TextField(
                blank=True,
                help_text="Now holds string for JSON data on import.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="allevents", name="start", field=models.CharField(max_length=90),
        ),
    ]
