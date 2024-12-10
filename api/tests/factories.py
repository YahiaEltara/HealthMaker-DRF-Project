import factory
from api.models import User, Coach, Client, Recommendation, Workout_Plan, Meal




class UserCoachFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"coach_user_{n}")  # Ensure unique usernames
    gender = 'male'
    age = 22
    role = 'coach'

class CoachFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coach

    user = factory.SubFactory(UserCoachFactory)
    gender = 'male'
    age = 22




class UserClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"client_user_{n}")  # Ensure unique usernames
    gender = 'female'
    age = 20
    role = 'client'

class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    user = factory.SubFactory(UserCoachFactory)
    gender = 'male'
    age = 22
    weight = 72
    height = 162
    goal = 'Special Program'




class RecommendationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recommendation

    client = factory.SubFactory(ClientFactory)
    coach = factory.SubFactory(CoachFactory)
    title = factory.Faker('text', max_nb_chars=25)  # Faker generates text within the max_length constraint
    details = "need more information about your breath test"



class WorkoutPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Workout_Plan

    client = factory.SubFactory(ClientFactory)
    coach = factory.SubFactory(CoachFactory)
    type = 'GYM & Cardio'
    details = "3 times/week"
    duration = "45-90"
    target_calories = 800



class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meal

    client = factory.SubFactory(ClientFactory)
    coach = factory.SubFactory(CoachFactory)
    workout_plan = factory.SubFactory(WorkoutPlanFactory)
    type = 'Breakfast'
    food_items = "Chicken - Eggs - Green"
    total_calories = 600
    eating_time = "09:00"



