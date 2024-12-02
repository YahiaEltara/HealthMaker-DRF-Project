from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import uuid
from django.contrib.auth.models import AbstractUser      , Group
# from .utils import ApiUserManager


class User(AbstractUser):
    GENDER_CHOICES= [('male', 'Male'),('female', 'Female')]
    ROLE_CHOICES = [('client', 'client'), ('coach', 'coach')]
    
    gender = models.CharField(max_length=20, choices= GENDER_CHOICES)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # objects = ApiUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
    class Meta:
        indexes = [
            models.Index(fields=  ['username', ]),
        ]

    
    
class Coach(models.Model):
    gender_choices= [('male', 'Male'),('female', 'Female')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, choices= gender_choices)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    class Meta:
        indexes = [
            models.Index(fields=  ['user', ]),
        ]



        
class Client(models.Model):
    GENDER_CHOICES= [('male', 'Male'),('female', 'Female')]
    GOAL_CHOICES= GOAL_CHOICES = [('Lose Weight', 'Lose Weight'), ('Build Muscles', 'Build Muscles'), ('Special Program', 'Special Program'),]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.PROTECT, related_name='clients')
    gender = models.CharField(max_length=20, choices= GENDER_CHOICES)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    weight = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(180)])
    height = models.PositiveIntegerField(validators=[MinValueValidator(50), MaxValueValidator(250)])
    goal = models.CharField(max_length=20, choices = GOAL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    class Meta:
        indexes = [
            models.Index(fields=  ['user', 'coach']),
        ]




class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'recommendation: {self.title} client: {str(self.client)} - coach: {str(self.coach)}'
    class Meta:
        indexes = [
            models.Index(fields=  ['client', 'coach']),
        ]





class Workout_Plan(models.Model):
    workout_choices=[
        ('GYM & Cardio', 'GYM & Cardio'),
        ('GYM', 'GYM'),
        ('Cardio', 'Cardio'),
        ('Special Sport', 'Special Sport'),]

    client = models.OneToOneField(Client, on_delete=models.CASCADE,  related_name='workout_plans')
    coach = models.ForeignKey(Coach, on_delete=models.PROTECT)
    type = models.CharField(max_length=255, choices= workout_choices)
    details = models.TextField()
    duration = models.TextField(help_text= 'minutes/once', max_length=255)
    target_calories = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, db_index=True)
    def save (self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.type}-{self.client}')
        super(Workout_Plan, self).save(*args, **kwargs)

    def __str__(self):
        return f'Workout Plan: "{str(self.type)}" - Client: {str(self.client)} - Coach: {str(self.coach)}'
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['type', 'client', ], name= 'unique_type'),
        ]
        indexes = [
            models.Index(fields=  ['client', 'coach']),
        ]
    





class Meal(models.Model):
    choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    workout_plan = models.ForeignKey(Workout_Plan, on_delete=models.PROTECT, related_name='meals')
    type = models.CharField(max_length=255, choices= choices)
    food_items = models.TextField()
    total_calories = models.FloatField()
    eating_time = models.TimeField()
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(blank=True, db_index=True)
    def save (self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.type}-{self.client}')
        super(Meal, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.type} for {self.client}'
    
    class Meta:
        ordering = ['eating_time']
        constraints = [
            models.UniqueConstraint(fields= ['type', 'client', 'coach', ], name= 'unique_meal_user'),
        ]
        indexes = [
            models.Index(fields=  ['type', 'workout_plan']),
        ]