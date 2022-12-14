# Generated by Django 4.1 on 2022-08-26 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0007_alter_js_url_skill'),
    ]

    operations = [
        migrations.CreateModel(
            name='skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('field', models.CharField(max_length=50)),
                ('base', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='roadmap.skills')),
            ],
        ),
        migrations.CreateModel(
            name='url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=255)),
                ('link_name', models.CharField(max_length=255)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='url', to='roadmap.skills')),
            ],
        ),
    ]
