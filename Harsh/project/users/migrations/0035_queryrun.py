# Generated by Django 4.0.2 on 2024-04-20 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_chathistory_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='', max_length=255, null=True)),
                ('user_query', models.TextField()),
                ('generated_sql_query', models.TextField()),
                ('query_result', models.TextField(null=True)),
            ],
        ),
    ]
