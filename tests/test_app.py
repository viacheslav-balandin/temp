from urllib.parse import quote


def activity_signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/signup"


def test_get_activities_returns_seeded_data(client):
    response = client.get("/activities")

    assert response.status_code == 200

    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["description"]
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_adds_new_participant(client):
    email = "new.student@mergington.edu"

    response = client.post(activity_signup_path("Chess Club"), params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        activity_signup_path("Chess Club"),
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        activity_signup_path("Unknown Club"),
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_existing_participant(client):
    response = client.delete(
        activity_signup_path("Science Club"),
        params={"email": "grace@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered grace@mergington.edu from Science Club"
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()["Science Club"]["participants"]
    assert "grace@mergington.edu" not in participants


def test_unregister_rejects_student_not_registered(client):
    response = client.delete(
        activity_signup_path("Science Club"),
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        activity_signup_path("Unknown Club"),
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}