# Generated by Django 4.2.2 on 2023-06-14 07:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0021_alter_user_username"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "managed": True,
                "ordering": ("-id",),
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.AlterModelTable(
            name="user",
            table="users_user",
        ),
    ]