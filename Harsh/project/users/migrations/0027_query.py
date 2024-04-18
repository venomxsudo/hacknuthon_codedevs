# Generated by Django 4.2.2 on 2023-06-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0026_alter_pendinguser_phone_alter_user_phonenumber"),
    ]

    operations = [
        migrations.CreateModel(
            name="Query",
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
                ("name", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                (
                    "location_latitude",
                    models.DecimalField(decimal_places=6, max_digits=9),
                ),
                (
                    "location_longitude",
                    models.DecimalField(decimal_places=6, max_digits=9),
                ),
                ("message", models.TextField()),
                ("photos", models.ImageField(upload_to="query_photos")),
                ("date", models.DateField()),
                ("time", models.TimeField()),
            ],
        ),
    ]