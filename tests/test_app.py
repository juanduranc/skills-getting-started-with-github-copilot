from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_rejected():
    email = "duplicate.student@example.com"
    response = client.post("/activities/Chess Club/signup?email=" + email)
    assert response.status_code == 200

    second_response = client.post("/activities/Chess Club/signup?email=" + email)
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up"


def test_unregister_participant_removes_email():
    email = "remove.student@example.com"
    client.post("/activities/Chess Club/signup?email=" + email)

    response = client.delete(f"/activities/Chess Club/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    activity = client.get("/activities").json()["Chess Club"]
    assert email not in activity["participants"]
