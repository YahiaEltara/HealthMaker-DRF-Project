from jsonschema import ValidationError
from .models import Client, Coach, Recommendation, Meal, Workout_Plan, User
from rest_framework import serializers
# from django.contrib.auth.models import User




# class UserRegistrationSerializer(serializers.Serializer):
#     role_choices=[('client', 'client'), ('coach', 'coach')]
#     gender_choices= [('male', 'Male'),('female', 'Female')]
#     goal_choices= [('Lose Weight', 'Lose Weight'),('Build Muscles', 'Build Muscles'), ('Specific Program', 'Specific Program')]

#     # Generic fields
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     role = serializers.ChoiceField(choices=role_choices)
#     gender = serializers.ChoiceField(choices=gender_choices,)
#     age = serializers.IntegerField()

#     # Specific fields in case of 'client' role
#     goal = serializers.ChoiceField(required=False, choices=goal_choices)
#     weight = serializers.FloatField(required=False)
#     height = serializers.FloatField(required=False)
#     coach = serializers.ChoiceField(required=False, choices=[])

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Dynamically populate the coach choices
#         self.fields['coach'].choices =  [
#             (coach, f"{coach.user.username} (Age: {coach.age}, Gender: {coach.gender})")
#             for coach in Coach.objects.all()    ]

#     def validate(self, data):
#         role = data.get('role')
#         if role == 'client':
#             if not data.get('goal') or not data.get('weight') or not data.get('height') or not data.get('coach'):
#                 raise serializers.ValidationError("Client fields (goal, weight, height, coach) are required.")
#         return data

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#         )
#         role = validated_data['role']
        
#         if role == 'client':
#             coach = validated_data['coach']
#             Client.objects.create(
#                 user=user, coach=coach, gender=validated_data.get('gender'), age=validated_data.get('age'),
#                 weight= validated_data.get('weight'), height= validated_data.get('height'), goal=validated_data.get('goal'),)
            
#         elif role == 'coach':
#             Coach.objects.create(
#                 user=user, gender=validated_data.get('gender'), age=validated_data.get('age'),)
            
#         return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'gender', 'age']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data, role=role)

        if role == 'client':
            Client.objects.create(
                user=user,
                gender=validated_data.get('gender'),
                age=validated_data.get('age'),
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

    class Meta:
        model = Workout_Plan
        fields = ['client', 'coach', 'type', 'details', 'duration', 'target_calories', 'slug', 'meals', ]
    def validate(self, data):
        # Check if a workout plan already exists for the client
        client = data.get('client')
        if Workout_Plan.objects.filter(client=client).exists():
            raise ValidationError({"message": "Each Client Can Have Only One Workout Plan .."})
        return data