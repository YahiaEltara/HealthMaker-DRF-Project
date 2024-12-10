from pytest_factoryboy import register
from . factories import UserCoachFactory, UserClientFactory, CoachFactory, ClientFactory, RecommendationFactory, WorkoutPlanFactory, MealFactory
import pytest
from rest_framework.test import APIClient



register(UserCoachFactory)
register(UserClientFactory)
register(CoachFactory)
register(ClientFactory)
register(RecommendationFactory)
register(WorkoutPlanFactory)
register(MealFactory)


@pytest.fixture
def api_client():
    return APIClient
