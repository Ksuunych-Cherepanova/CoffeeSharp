# Generated by Django 4.2.1 on 2025-03-24 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['-time_create']},
        ),
        migrations.AddField(
            model_name='menu',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255),
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['-time_create'], name='menu_menu_time_cr_0d8fe4_idx'),
        ),
    ]
