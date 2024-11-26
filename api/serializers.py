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
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='user__username')
    coaches = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='user__username')

    class Meta:
        model = Workoutplan
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['id']
        for field in exclude_fields:
            self.fields.pop(field, None)


class MealSerializer(serializers.ModelSerializer):
    workout_plans = serializers.SlugRelatedField(queryset=Workoutplan.objects.all(), slug_field='name')

    class Meta:
        model = Meal
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['id']
        for field in exclude_fields:
            self.fields.pop(field, None)

