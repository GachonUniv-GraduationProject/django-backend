# Generated by Django 4.1 on 2022-12-01 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_profile_is_individual"),
    ]

    operations = [
        migrations.CreateModel(
            name="Roadmap",
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
                ("field_name", models.CharField(blank=True, max_length=200)),
                ("progress", models.CharField(blank=True, max_length=200)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="roadmap",
                        to="account.profile",
                    ),
                ),
            ],
        ),
    ]
