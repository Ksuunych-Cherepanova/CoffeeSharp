# Generated by Django 4.2.1 on 2025-04-07 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_category_menu_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='menu.category'),
        ),
    ]
