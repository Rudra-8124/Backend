"""
tests/test_users.py  —  Tests for /users endpoints
"""
from unittest.mock import patch
from tests.conftest import client, ADMIN_USER, ANALYST_USER, VIEWER_USER
from app.core.security import create_access_token
from datetime import timedelta


def _auth(user):
    token = create_access_token({"sub": user["id"]}, expires_delta=timedelta(minutes=30))
    return {"Authorization": f"Bearer {token}"}


def _mock_user(user):
    return patch("app.services.user_service.fetch_data", return_value=[user])


NEW_USER_PAYLOAD = {
    "name": "New Analyst",
    "email": "new@example.com",
    "password": "securepassword123",
    "role": "ANALYST",
    "is_active": True,
}

CREATED_USER = {
    **NEW_USER_PAYLOAD,
    "id": "44444444-4444-4444-4444-444444444444",
    "created_at": "2024-06-01T00:00:00",
    "password": "hashed_pw",
}


class TestCreateUser:
    def test_admin_can_create_user(self):
        with _mock_user(ADMIN_USER):
            with patch("app.services.user_service.fetch_data", side_effect=[[ADMIN_USER], [], [CREATED_USER]]):
                with patch("app.services.user_service.insert_data", return_value=CREATED_USER):
                    resp = client.post("/users/", json=NEW_USER_PAYLOAD, headers=_auth(ADMIN_USER))
        assert resp.status_code == 201

    def test_analyst_cannot_create_user(self):
        with _mock_user(ANALYST_USER):
            resp = client.post("/users/", json=NEW_USER_PAYLOAD, headers=_auth(ANALYST_USER))
        assert resp.status_code == 403

    def test_viewer_cannot_create_user(self):
        with _mock_user(VIEWER_USER):
            resp = client.post("/users/", json=NEW_USER_PAYLOAD, headers=_auth(VIEWER_USER))
        assert resp.status_code == 403

    def test_duplicate_email_rejected(self):
        """Creating a user with an existing email returns 400."""
        with patch("app.services.user_service.fetch_data", side_effect=[[ADMIN_USER], [ADMIN_USER]]):
            resp = client.post("/users/", json=NEW_USER_PAYLOAD, headers=_auth(ADMIN_USER))
        assert resp.status_code == 400

    def test_invalid_email_rejected(self):
        with _mock_user(ADMIN_USER):
            payload = {**NEW_USER_PAYLOAD, "email": "not-an-email"}
            resp = client.post("/users/", json=payload, headers=_auth(ADMIN_USER))
        assert resp.status_code == 422


class TestGetUsers:
    def test_admin_can_list_users(self):
        with patch("app.services.user_service.fetch_data", side_effect=[[ADMIN_USER], [ADMIN_USER, ANALYST_USER]]):
            resp = client.get("/users/", headers=_auth(ADMIN_USER))
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_analyst_cannot_list_users(self):
        with _mock_user(ANALYST_USER):
            resp = client.get("/users/", headers=_auth(ANALYST_USER))
        assert resp.status_code == 403

    def test_get_user_by_id(self):
        with patch("app.services.user_service.fetch_data", side_effect=[[ADMIN_USER], [ANALYST_USER]]):
            resp = client.get(f"/users/{ANALYST_USER['id']}", headers=_auth(ADMIN_USER))
        assert resp.status_code == 200

    def test_get_unknown_user_returns_404(self):
        with patch("app.services.user_service.fetch_data", side_effect=[[ADMIN_USER], []]):
            resp = client.get("/users/nonexistent-id", headers=_auth(ADMIN_USER))
        assert resp.status_code == 404

    def test_get_me(self):
        with _mock_user(ADMIN_USER):
            resp = client.get("/users/me", headers=_auth(ADMIN_USER))
        assert resp.status_code == 200
        assert resp.json()["email"] == ADMIN_USER["email"]


class TestUserStatus:
    def test_admin_can_deactivate_user(self):
        deactivated = {**ANALYST_USER, "is_active": False}
        with patch("app.services.user_service.fetch_data", side_effect=[[ADMIN_USER], [ANALYST_USER]]):
            with patch("app.services.user_service.update_data", return_value=deactivated):
                resp = client.patch(
                    f"/users/{ANALYST_USER['id']}/status?is_active=false",
                    headers=_auth(ADMIN_USER),
                )
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

    def test_analyst_cannot_change_status(self):
        with _mock_user(ANALYST_USER):
            resp = client.patch(
                f"/users/{VIEWER_USER['id']}/status?is_active=false",
                headers=_auth(ANALYST_USER),
            )
        assert resp.status_code == 403
