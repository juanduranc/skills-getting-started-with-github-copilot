from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_rejected():
    # Arrange
    email = "duplicate.student@example.com"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)
    second_response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"


def test_unregister_participant_removes_email():
    # Arrange
    email = "remove.student@example.com"
    client.post("/activities/Chess Club/signup?email=" + email)

    # Act
    response = client.delete(f"/activities/Chess Club/participants/{email}")
    activity = client.get("/activities").json()["Chess Club"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in activity["participants"]
