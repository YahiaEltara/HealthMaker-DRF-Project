from .models import Client, Coach, Recommendation, Meal, Workoutplan
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
    workout_plan = serializers.SlugRelatedField(queryset=Workoutplan.objects.all(), slug_field='name')

    class Meta:
        model = Meal
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['id']
        for field in exclude_fields:
            self.fields.pop(field, None)


class WorkoutplanSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='user__username')
    coach = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='user__username')
    meals = MealSerializer(many=True, read_only=True)

    class Meta:
        model = Workoutplan
        fields = ['client', 'coach', 'name', 'details', 'duration', 'target_calories_burned', 'created_at', 'slug', 'meals', ]