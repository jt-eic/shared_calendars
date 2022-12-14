# Generated by Django 4.1 on 2022-09-06 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_allevents_other_ids"),
    ]

    operations = [
        migrations.AddField(
            model_name="allevents",
            name="usershare1",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="allevents",
            name="usershare2",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="allevents",
            name="usershare3",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="allevents",
            name="usershare4",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="allevents",
            name="other_ids",
            field=models.TextField(
                blank=True,
                help_text="not used here, unless json works. use single fields.",
                null=True,
            ),
        ),
    ]
