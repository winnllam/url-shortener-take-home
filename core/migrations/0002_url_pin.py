# Generated by Django 4.2.3 on 2023-09-11 00:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="url",
            name="pin",
            field=models.CharField(blank=True, max_length=4),
        ),
    ]