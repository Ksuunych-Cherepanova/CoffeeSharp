# Generated by Django 4.2.1 on 2025-04-20 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_alter_menugallerycover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='days_count',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
