# Generated by Django 4.1 on 2022-08-21 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0002_remove_data_experience_level_data_career_min'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='expiration',
        ),
        migrations.AddField(
            model_name='data',
            name='api_id',
            field=models.IntegerField(default=0),
        ),
    ]
