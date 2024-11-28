from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import uuid



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
    class Meta:
        indexes = [
            models.Index(fields=  ['user', 'coach']),
        ]




class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=20)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    gender = models.CharField(max_length=255, choices= [('male', 'Male'),('female', 'Female')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    class Meta:
        indexes = [
            models.Index(fields=  ['user', ]),
        ]




class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="recommendation_client")
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name="recommendation_coach")
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'client: {str(self.client)} - coach: {str(self.coach)} recommendation'
    class Meta:
        indexes = [
            models.Index(fields=  ['client', 'coach']),
        ]





class Workoutplan(models.Model):
    client = models.OneToOneField(Client, max_length=255, on_delete=models.CASCADE, related_name="workoutplan")
    coach = models.ForeignKey(Coach, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    details = models.TextField()
    duration = models.TextField(help_text= 'minutes/once', max_length=255)
    target_calories_burned = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, db_index=True)
    def save (self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        super(Workoutplan, self).save(*args, **kwargs)

    def __str__(self):
        return f'Workout Plan: "{str(self.name)}" - client: {str(self.client)} - coach: {str(self.coach)}'
    class Meta:
        indexes = [
            models.Index(fields=  ['client', 'coach']),
        ]
    





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
    workout_plan = models.ForeignKey(Workoutplan, on_delete=models.PROTECT, related_name= 'meals', blank= True, null=True)
    slug = models.SlugField(blank=True, db_index=True)
    def save (self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.meal_type)
        super(Meal, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.meal_type} for {self.workout_plan.client}'
    
    class Meta:
        ordering = ['eating_time']
        constraints = [
            models.UniqueConstraint(fields= ['meal_type', 'workout_plan'], name= 'unique_meal_user'),
        ]
        indexes = [
            models.Index(fields=  ['meal_type', 'workout_plan']),
        ]