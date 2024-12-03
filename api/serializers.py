from rest_framework.exceptions import ValidationError
from .models import Client, Coach, Recommendation, Meal, Workout_Plan, User
from rest_framework import serializers
# from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    weight = serializers.FloatField(required=False, allow_null=True)
    height = serializers.FloatField(required=False, allow_null=True)
    fitness_goal = serializers.ChoiceField(choices=Client.GOAL_CHOICES, required=False, allow_blank=True)
    coach = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'gender', 'age', 'weight', 'height', 'fitness_goal', 'coach']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        """
        Ensure required fields are provided based on the role.
        """
        role = attrs.get('role')
        if role == 'client':
            missing_fields = []
            if attrs.get('weight') is None:
                missing_fields.append('weight')
            if attrs.get('height') is None:
                missing_fields.append('height')
            if attrs.get('fitness_goal') is None:
                missing_fields.append('fitness_goal')
            if attrs.get('height') is None:
                missing_fields.append('height')
            if not attrs.get('coach'):
                missing_fields.append('coach')

            if missing_fields:
                raise serializers.ValidationError(
                    {field: f"{field} is required for the 'client' role." for field in missing_fields})
    
            coach_username = attrs.get('coach')
            try:
                coach_user = User.objects.get(username=coach_username)
                if not hasattr(coach_user, 'coach'):
                    raise serializers.ValidationError({'coach': 'The provided username does not belong to a coach.'})
            except User.DoesNotExist:
                raise serializers.ValidationError({'coach': 'No user found with the provided username.'})

            attrs['coach'] = coach_user.coach  # Replace username with Coach object

        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        weight = validated_data.pop('weight', None)
        height = validated_data.pop('height', None)
        fitness_goal = validated_data.pop('fitness_goal', None)
        coach = validated_data.pop('coach', None)

        user = User.objects.create_user(**validated_data, role=role)

        if role == 'client':
            Client.objects.create(
                user=user, coach = coach, gender=validated_data.get('gender'), age=validated_data.get('age'),
                weight=weight, height=height, goal=fitness_goal
            )
        elif role == 'coach':
            Coach.objects.create(
                user=user,
                gender=validated_data.get('gender'),
                age=validated_data.get('age'),
            )

        return user
    
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
    type = serializers.ChoiceField(choices=Workout_Plan.WORKOUT_CHOICES)  # Automatically validates against choices

    class Meta:
        model = Workout_Plan
        fields = ['client', 'coach', 'type', 'details', 'duration', 'target_calories', 'slug', 'meals', ]
    def validate(self, data):
        """
        Check if a workout plan already exists for the provided client in POST request
        """
        request_method = self.context['request'].method  # Get the request method (POST/PUT)
        client = data.get('client')
        coach = data.get('coach')
        
        if request_method == 'POST':  # Validation logic for POST request

            if client.coach != coach:
                raise ValidationError({"message": "The provided coach does not match the client's assigned coach."})
            if Workout_Plan.objects.filter(client=client).exists():
                raise ValidationError({"message": "This client already has a workout plan .."})
            
        return data