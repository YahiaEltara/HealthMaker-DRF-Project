from jsonschema import ValidationError
from .models import Client, Coach, Recommendation, Meal, Workout_Plan
from rest_framework import serializers


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
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='user__username')
    coach = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='user__username')
    workout_plan = serializers.SlugRelatedField(queryset=Workout_Plan.objects.all(), slug_field='type')

    class Meta:
        model = Meal
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_fields = ['id', 'created_at',]
        for field in exclude_fields:
            self.fields.pop(field, None)


class Workout_PlanSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='user__username')
    coach = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='user__username')
    meals = MealSerializer(many=True, read_only=True)

    class Meta:
        model = Workout_Plan
        fields = ['client', 'coach', 'type', 'details', 'duration', 'target_calories', 'slug', 'meals', ]
    def validate(self, data):
        # Check if a workout plan already exists for the client
        client = data.get('client')
        if Workout_Plan.objects.filter(client=client).exists():
            raise ValidationError({"message": "Each Client Can Have Only One Workout Plan .."})
        return data