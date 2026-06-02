from urllib.parse import quote


def test_unregister_removes_existing_participant(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"

    response = client.delete(
        f"/activities/{quote(activity, safe='')}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email not in participants


def test_unregister_returns_404_for_missing_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}