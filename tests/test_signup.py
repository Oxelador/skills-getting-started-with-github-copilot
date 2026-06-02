from urllib.parse import quote


def test_signup_adds_new_participant(client):
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    response = client.post(
        f"/activities/{quote(activity, safe='')}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email in participants


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}