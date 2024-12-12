import pytest
import json
from rest_framework import status

@pytest.mark.django_db
class TestClientViewSet:
    endpoint = "/api/clients/"

    def test_unauthenticated_user(self, api_client):
        # Arrange: Unauthenticated user
        client = api_client()
        # Act
        response = client.get(self.endpoint)
        # Assert: Unauthorized access
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_client_user(self, api_client, user_client_factory, client_factory, user_coach_factory ,coach_factory):

        # Arrange: Authenticate as a client user and ensure linked Client instance
        client_user = user_client_factory(role='client')  # Create client_user instance
        coach_user  = user_coach_factory(role='coach')     # Create coach_user instance
        coach = coach_factory(user=coach_user)            # Create associated Coach instance
        client_factory(user=client_user, coach=coach)  # Create associated Client instance

        client = api_client()
        client.force_authenticate(user=client_user)
        # Act
        response = client.get(self.endpoint)
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_client_user_allowed_methods(self, api_client, user_client_factory, client_factory, user_coach_factory ,coach_factory):
        # Arrange: Authenticate as a client user
        client_user = user_client_factory(role='client')
        coach_user  = user_coach_factory(role='coach')     # Create coach_user instance
        coach = coach_factory(user=coach_user)            # Create associated Coach instance
        client = client_factory(user=client_user, coach=coach)

        client_built = api_client()
        client_built.force_authenticate(user=client_user)

        # Case 1: Test GET
        response_get = client_built.get(f"{self.endpoint}{client.user.username}/")
        assert response_get.status_code == status.HTTP_200_OK

        # Case 2: Test PUT (Allowed)
        update_data = {
            "user" : client_user.username,
            "coach" : coach_user.username,
            "gender": "female",
            "age": 25,
            "weight": 80,
            "height": 170,
            "goal": "Special Program"
        }
        response_put = client_built.put(f"{self.endpoint}{client.user.username}/", data=update_data, format="json")
        assert response_put.status_code == status.HTTP_200_OK

        # Case 3: Test DELETE (Allowed)
        response_delete = client_built.delete(f"{self.endpoint}{client.user.username}/")
        assert response_delete.status_code == status.HTTP_204_NO_CONTENT

        # Case 4: Test POST (Not allowed for client users)
        post_data = {
            "gender": "male",
            "age": 30,
            "weight": 80,
            "height": 170,
            "goal": "New Goal",
        }
        response_post = client_built.post(self.endpoint, data=post_data, format="json")
        assert response_post.status_code == status.HTTP_403_FORBIDDEN
