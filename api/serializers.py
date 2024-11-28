from .models import Client, Coach, Recommendation, Meal, Workoutplan
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='username')
    coach = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='user__username')
    class Meta:
        model = Client
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['id', 'created_at',]
        for field in exclude_fields:
            self.fields.pop(field, None)


class CoachSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='username')

    class Meta:
        model = Coach
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['id', 'created_at',]
        for field in exclude_fields:
            self.fields.pop(field, None)


class RecommendationSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='user__username')
    coach = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='user__username')
    class Meta:
        model = Recommendation
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['created_at',]
        for field in exclude_fields:
            self.fields.pop(field, None)


class MealSerializer(serializers.ModelSerializer):
    workout_plan = serializers.SlugRelatedField(queryset=Workoutplan.objects.all(), slug_field='name')

    class Meta:
        model = Meal
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['id', 'created_at',]
        for field in exclude_fields:
            self.fields.pop(field, None)


class WorkoutplanSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='user__username')
    coach = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='user__username')
    meals = MealSerializer(many=True, read_only=True)

    class Meta:
        model = Workoutplan
        fields = ['client', 'coach', 'name', 'details', 'duration', 'target_calories_burned', 'slug', 'meals', ]