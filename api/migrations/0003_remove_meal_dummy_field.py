# Generated by Django 5.1.3 on 2024-11-25 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_meal_dummy_field_alter_meal_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='dummy_field',
        ),
    ]