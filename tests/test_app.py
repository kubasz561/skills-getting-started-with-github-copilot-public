from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    email = "student-delete@example.com"
    activity_name = "Chess Club"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200

    data = response.json()
    assert "Removed" in data["message"]

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_not_found_when_missing():
    response = client.delete("/activities/Chess Club/participants/missing@example.com")

    assert response.status_code == 404
