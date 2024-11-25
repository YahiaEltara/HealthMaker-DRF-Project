from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver



class Client(models.Model):
    choices = (
        ('maintain', 'Maintain'),
        ('lose weight', 'Lose Weight'),
        ('gain muscle', 'Gain Muscle'),
        ('build muscle', 'Build Muscle'),)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=20)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    gender = models.CharField(max_length=255, choices= [('male', 'Male'),('female', 'Female')])
    weight = models.FloatField()
    height = models.FloatField()
    fitness_goal = models.CharField(max_length=255, choices= choices)
    created_at = models.DateTimeField(auto_now_add=True)
    coach = models.ForeignKey('Coach', on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username





class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=20)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    gender = models.CharField(max_length=255, choices= [('male', 'Male'),('female', 'Female')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username




class Recommendation(models.Model):
    clients = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="recommendation_clients")
    coaches = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name="recommendation_coaches")
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'client: {str(self.clients)} - coach: {str(self.coaches)} recommendation'





class Workoutplan(models.Model):
    client = models.OneToOneField(Client, max_length=255, on_delete=models.CASCADE, related_name="workoutplans")
    coaches = models.ForeignKey(Coach, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    details = models.TextField()
    duration = models.TextField(help_text= 'minutes/once', max_length=255)
    target_calories_burned = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'client: {str(self.client)} - coach: {str(self.coaches)} - Workout Plan'





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

    def __str__(self):
        return f'{self.meal_type} for {self.workout_plans.client}'