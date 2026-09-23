from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Soccer Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200, signup_response.text

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 200, response.text

    payload = response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]


def test_unregister_for_unknown_email_returns_404():
    response = client.delete("/activities/Soccer Club/participants?email=missing@mergington.edu")
    assert response.status_code == 404, response.text
