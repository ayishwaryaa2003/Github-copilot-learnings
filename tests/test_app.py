from urllib.parse import quote

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_signup_and_unregister_workflow():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = list(app_module.activities[activity_name]["participants"])

    try:
        response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")
        assert response.status_code == 200
        assert email in app_module.activities[activity_name]["participants"]

        unregister_response = client.delete(f"/activities/{quote(activity_name)}/signup?email={email}")
        assert unregister_response.status_code == 200
        assert email not in app_module.activities[activity_name]["participants"]
    finally:
        app_module.activities[activity_name]["participants"] = original_participants


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
