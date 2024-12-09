import pytest
pytestmark = pytest.mark.django_db
from django.core.exceptions import ValidationError
from api.models import User, Coach, Client, Recommendation, Workout_Plan, Meal



class TestUserCoachModel:
    def test_valid_user_creation(self):
        # Arrange & Act
        user = User.objects.create(
            username="coach_user",
            gender="male",
            age=22,
            role="coach",
        )
        # Assert
        assert user.username == "coach_user"
        assert user.gender == "male"
        assert user.age == 22
        assert user.role == "coach"

    def test_invalid_age(self):
        # Arrange
        user = User(
            username="invalidageuser",
            gender="male",
            age=150,  # Invalid age
            role="coach",
        )
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()  # Trigger field validation

    def test_invalid_gender_choice(self):
        # Arrange
        user = User(
            username="invalidgender",
            gender="unknown",  # Invalid choice
            age=30,
            role="coach",
        )
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_missing_required_field(self):
        # Arrange
        user = User(
            gender="male",
            age=25,
            role="coach",
        )  # Missing `username`
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_str_method(self, user_coach_factory):
        # Arrange
        obj = user_coach_factory(username="aser")  # Create a user instance using the factory
        # Act & Assert
        assert str(obj) == "aser"


class TestUserClientModel:
    def test_valid_user_creation(self):
        # Arrange & Act
        user = User.objects.create(
            username="client_user",
            gender="male",
            age=22,
            role="client",
        )
        # Assert
        assert user.username == "client_user"
        assert user.gender == "male"
        assert user.age == 22
        assert user.role == "client"

    def test_invalid_age(self):
        # Arrange
        user = User(
            username="invalidageuser",
            gender="male",
            age=150,  # Invalid age
            role="client",
        )
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()  # Trigger field validation

    def test_invalid_gender_choice(self):
        # Arrange
        user = User(
            username="invalidgender",
            gender="unknown",  # Invalid choice
            age=30,
            role="client",
        )
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_missing_required_field(self):
        # Arrange
        user = User(
            gender="male",
            age=25,
            role="client",
        )  # Missing `username`
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_str_method(self, user_client_factory):
        # Arrange
        obj = user_client_factory(username="client_user")  # Create a user instance using the factory
        # Act & Assert
        assert str(obj) == "client_user"


class TestCoachModel:
    def test_valid_user_creation(self, user_coach_factory):
        # Arrange & Act
        user = user_coach_factory()
        user = Coach.objects.create(
            user= user,
            gender="male",
            age=22,
        )
        # Assert
        assert user == user
        assert user.gender == "male"
        assert user.age == 22

    def test_invalid_age(self, user_coach_factory):
        # Arrange
        user = user_coach_factory()
        user = Coach(
            user=user,
            gender="male",
            age=150,  # Invalid age
        )
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()  # Trigger field validation

    def test_invalid_gender_choice(self, user_coach_factory):
        # Arrange
        user = user_coach_factory()
        user = Coach(
            user=user,
            gender="unknown",  # Invalid choice
            age=30,
        )
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_missing_required_field(self):
        # Arrange
        user = Coach(
            gender="male",
            age=25,
        )  # Missing `username`
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_str_method(self, user_coach_factory):
        # Arrange
        obj = user_coach_factory(username="coach_user")  # Create a user instance using the factory
        # Act & Assert
        assert str(obj) == "coach_user"


class TestClientModel:
    def test_valid_user_creation(self, user_client_factory, coach_factory):
        # Arrange & Act
        user = user_client_factory()  # Create a coach_user instance using the factory
        coach = coach_factory()  # Create a coach instance using the factory
        user = Client.objects.create(
            user= user,
            coach = coach,
            gender="male",
            age=22,
            weight = 72,
            height = 162
        )
        # Assert
        assert user.coach == coach
        assert user.gender == "male"
        assert user.age == 22
        assert user.weight == 72
        assert user.height == 162

    def test_invalid_age(self, user_client_factory, coach_factory):
        # Arrange
        user = user_client_factory()  # Create a coach_user instance using the factory
        coach = coach_factory()  # Create a coach instance using the factory
        user = Client(
            user= user,
            coach = coach,
            gender="male",
            age=150,
            weight = 72,
            height = 162
        )
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()  # Trigger field validation

    def test_invalid_gender_choice(self, user_client_factory, coach_factory):
        # Arrange
        user = user_client_factory()  # Create a coach_user instance using the factory
        coach = coach_factory()  # Create a coach instance using the factory
        user = Client(
            user= user,
            coach = coach,
            gender="unknown",
            age=22,
            weight = 72,
            height = 162
        )
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_missing_required_field(self, user_client_factory):
        # Arrange
        user = user_client_factory()  # Create a coach_user instance using the factory
        user = Client(
            user= user,
            gender="male",
            age=22,
            weight = 72,
            height = 162
        )  # Missing `username`
        # Act & Assert
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_str_method(self, user_client_factory):
        # Arrange
        obj = user_client_factory(username="client_user")  # Create a user instance using the factory
        # Act & Assert
        assert str(obj) == "client_user"


class TestRecommendationModel:
    def test_valid_recommendation_creation(self, client_factory, coach_factory):
        coach = coach_factory()
        client = client_factory(coach=coach)
        object = Recommendation.objects.create(
            client = client,
            coach = coach,
            title="Sample Title",
            details="Sample Description",
        )
        assert object.client == client
        assert object.coach == coach
        assert object.title == "Sample Title"
        assert object.details == "Sample Description"

    def test_missing_required_field(self, client_factory, coach_factory):
        coach = coach_factory()
        client = client_factory(coach=coach)
        object = Recommendation(
            client = client,
            coach = coach,
            title="Sample Title",
        ) # Missing 'details' field
        with pytest.raises(ValidationError) as exc_info:
            object.full_clean()
        print(exc_info.value)


class TestWorkoutPlanModel:
    def test_valid_Workout_Plan_creation(self, client_factory, coach_factory):
        coach = coach_factory()
        client = client_factory(coach=coach)
        object = Workout_Plan.objects.create(
            client = client,
            coach = coach,
            type="Breakfast",
            details="Sample Description",
            duration = "45-90",
            target_calories = 800
        )
        assert object.client == client
        assert object.coach == coach
        assert object.details == "Sample Description"
        assert object.duration == "45-90"
        assert object.target_calories == 800

    def test_missing_required_field(self, client_factory, coach_factory):
        coach = coach_factory()
        client = client_factory(coach=coach)
        object = Workout_Plan(
            client = client,
            coach = coach,
            details="Sample Description",
            duration = "45-90",
            target_calories = 800
        )  # Missing `type`
        with pytest.raises(ValidationError) as exc_info:
            object.full_clean()
        print(exc_info.value)


class TestMealPlanModel:
    def test_valid_meal_creation(self, client_factory, coach_factory, workout_plan_factory):
        coach = coach_factory()
        client = client_factory(coach=coach)
        workout_plan = workout_plan_factory(client=client, coach=coach)
        object = Meal.objects.create(
            client = client,
            coach = coach,
            workout_plan = workout_plan,
            type="Breakfast",
            food_items = "Chicken - Eggs - Green",
            total_calories = 600,
            eating_time = "09:00"
        )
        assert object.client == client
        assert object.coach == coach
        assert object.workout_plan == workout_plan
        assert object.type == "Breakfast"
        assert object.food_items == "Chicken - Eggs - Green"
        assert object.total_calories == 600
        assert object.eating_time == "09:00"

    def test_missing_required_field(self, client_factory, coach_factory, workout_plan_factory):
        coach = coach_factory()
        client = client_factory(coach=coach)
        workout_plan = workout_plan_factory(client=client, coach=coach)
        object = Meal(
            client = client,
            coach = coach,
            type="Breakfast",
            food_items = "Chicken - Eggs - Green",
            total_calories = 600,
            eating_time = "09:00"
        )  # Missing `workout_plan`
        with pytest.raises(ValidationError) as exc_info:
            object.full_clean()
        print(exc_info.value)






