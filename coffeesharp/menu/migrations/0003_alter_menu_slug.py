# Generated by Django 4.2.1 on 2025-03-24 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_menu_options_menu_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
