# Generated by Django 4.1 on 2022-08-25 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0005_alter_js_url_skill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='javascript',
            old_name='child_skills',
            new_name='base',
        ),
        migrations.AlterField(
            model_name='js_url',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_skill', to='roadmap.javascript'),
        ),
    ]
