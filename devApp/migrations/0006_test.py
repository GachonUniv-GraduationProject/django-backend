# Generated by Django 4.1 on 2022-08-08 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devApp', '0005_delete_dummy_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('address', models.TextField()),
                ('nickname', models.TextField()),
            ],
        ),
    ]
