# Generated by Django 4.2.2 on 2023-06-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_alter_user_phonenumber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phonenumber",
            field=models.CharField(default=None, max_length=20),
        ),
    ]