# Generated by Django 4.1 on 2022-12-05 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0013_alter_field_name_alter_field_preference"),
    ]

    operations = [
        migrations.AlterField(
            model_name="field",
            name="name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="field",
            name="preference",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="roadmap",
            name="field_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="roadmap",
            name="progress",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
