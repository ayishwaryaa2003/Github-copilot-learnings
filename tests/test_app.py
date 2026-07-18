from urllib.parse import quote

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_signup_and_unregister_workflow():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = list(app_module.activities[activity_name]["participants"])

    try:
        # Act: sign up the student
        signup_response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

        # Assert: the signup succeeded and the participant was added
        assert signup_response.status_code == 200
        assert signup_response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert email in app_module.activities[activity_name]["participants"]

        # Act: unregister the student
        unregister_response = client.delete(f"/activities/{quote(activity_name)}/signup?email={email}")

        # Assert: the unregister succeeded and the participant was removed
        assert unregister_response.status_code == 200
        assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in app_module.activities[activity_name]["participants"]
    finally:
        app_module.activities[activity_name]["participants"] = original_participants


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
