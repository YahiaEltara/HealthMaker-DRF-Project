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


class WorkoutplanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workoutplan
        fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            exclude_fields = ['id']
            for field in exclude_fields:
                self.fields.pop(field, None)

