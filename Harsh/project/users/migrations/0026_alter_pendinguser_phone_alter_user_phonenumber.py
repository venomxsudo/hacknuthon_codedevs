# Generated by Django 4.2.2 on 2023-06-21 07:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0025_pendinguser_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pendinguser",
            name="phone",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="phonenumber",
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
