# Generated by Django 5.1.3 on 2024-11-25 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_meal_dummy_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
