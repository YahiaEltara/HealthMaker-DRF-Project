# Generated by Django 5.1.3 on 2024-11-25 08:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=20)),
                ('age', models.PositiveIntegerField(max_length=2)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=20)),
                ('age', models.PositiveIntegerField(max_length=2)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=255)),
                ('weight', models.FloatField()),
                ('height', models.FloatField()),
                ('fitness_goal', models.CharField(choices=[('maintain', 'Maintain'), ('lose weight', 'Lose Weight'), ('gain muscle', 'Gain Muscle'), ('build muscle', 'Build Muscle')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommendation_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendation_clients', to='api.client')),
                ('coaches', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendation_coaches', to='api.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Workoutplan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('duration', models.PositiveIntegerField()),
                ('calories_burned', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.OneToOneField(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='workoutplans', to='api.client')),
                ('coaches', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_type', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')], max_length=255)),
                ('food_items', models.TextField()),
                ('total_calories', models.FloatField()),
                ('eating_time', models.TimeField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('workout_plans', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.workoutplan')),
            ],
        ),
    ]
