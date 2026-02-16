from urllib.parse import quote
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_signup_and_remove_participant():
    activity = "Basketball Team"
    email = "test_user@example.com"

    # Ensure participant not present
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify present
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Remove
    resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # Verify removed
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]
