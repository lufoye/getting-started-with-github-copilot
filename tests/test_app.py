import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    # Try unregistering again (should fail)
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
