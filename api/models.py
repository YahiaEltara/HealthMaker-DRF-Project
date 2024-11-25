from django.db import models
from django.contrib.auth.models import User




class Client(models.Model):
    choices = (
        ('maintain', 'Maintain'),
        ('lose weight', 'Lose Weight'),
        ('gain muscle', 'Gain Muscle'),
        ('build muscle', 'Build Muscle'),)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=20)
    age = models.PositiveIntegerField(max_length=2)
    gender = models.CharField(max_length=255, choices= [('male', 'Male'),('female', 'Female')])
    weight = models.FloatField()
    height = models.FloatField()
    fitness_goal = models.CharField(max_length=255, choices= choices)
    created_at = models.DateTimeField(auto_now_add=True)
    coach = models.ForeignKey('Coach', on_delete=models.PROTECT)





class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=20)
    age = models.PositiveIntegerField(max_length=2)
    gender = models.CharField(max_length=255, choices= [('male', 'Male'),('female', 'Female')])
    created_at = models.DateTimeField(auto_now_add=True)





class Recommendation(models.Model):
    clients = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="recommendation_clients")
    coaches = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name="recommendation_coaches")
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)





class Workoutplan(models.Model):
    client = models.OneToOneField(Client, max_length=255, on_delete=models.CASCADE, related_name="workoutplans")
    coaches = models.ForeignKey(Coach, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    details = models.TextField()
    duration = models.PositiveIntegerField()
    calories_burned = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)





class Meal(models.Model):
    choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),]

    meal_type = models.CharField(max_length=255, choices= choices)
    food_items = models.TextField()
    total_calories = models.FloatField()
    eating_time = models.TimeField()
    created_at = models.DateField(auto_now_add=True)
    workout_plans = models.ForeignKey(Workoutplan, on_delete=models.PROTECT)