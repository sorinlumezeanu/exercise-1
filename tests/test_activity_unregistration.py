from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def reset_activities():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Basketball Team"]["participants"] = []


def test_unregister_participant_removes_email():
    reset_activities()

    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "daniel@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_participant_rejects_missing_email():
    reset_activities()

    response = client.delete(
        "/activities/Basketball Team/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
