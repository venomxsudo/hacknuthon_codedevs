# Generated by Django 4.0.2 on 2024-04-20 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_chathistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='chathistory',
            name='user',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
