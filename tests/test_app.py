import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities data before each test."""
    activities.clear()
    activities.update({
        "Sample Activity": {
            "description": "A sample activity for testing",
            "schedule": "Mondays, 3:00 PM - 4:00 PM",
            "max_participants": 10,
            "participants": []
        }
    })

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_register_participant():
    activity_name = "Sample Activity"
    email = "test@example.com"
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    assert "message" in response.json()


def test_unregister_participant():
    activity_name = "Sample Activity"
    email = "test@example.com"
    # First, register the participant
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Then, unregister the participant
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200
    assert "message" in response.json()