# Generated by Django 4.1 on 2022-08-25 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0004_alter_js_url_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='js_url',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='roadmap.javascript'),
        ),
    ]
