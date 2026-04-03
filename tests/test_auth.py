"""
tests/test_auth.py  —  Tests for POST /auth/login
"""
import pytest
from unittest.mock import patch
from tests.conftest import client, ADMIN_USER


class TestLogin:
    """Test suite for /auth/login"""

    def test_login_success(self):
        """Valid credentials return a bearer token."""
        with patch("app.services.user_service.fetch_data", return_value=[ADMIN_USER]):
            response = client.post(
                "/auth/login",
                data={"username": "admin@example.com", "password": "secret"},
            )
        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_login_wrong_password(self):
        """Wrong password returns 401."""
        with patch("app.services.user_service.fetch_data", return_value=[ADMIN_USER]):
            response = client.post(
                "/auth/login",
                data={"username": "admin@example.com", "password": "wrongpassword"},
            )
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect email or password"

    def test_login_unknown_email(self):
        """Unknown email returns 401."""
        with patch("app.services.user_service.fetch_data", return_value=[]):
            response = client.post(
                "/auth/login",
                data={"username": "ghost@example.com", "password": "secret"},
            )
        assert response.status_code == 401

    def test_login_deactivated_user(self):
        """Deactivated user cannot login."""
        inactive_user = {**ADMIN_USER, "is_active": False}
        with patch("app.services.user_service.fetch_data", return_value=[inactive_user]):
            response = client.post(
                "/auth/login",
                data={"username": "admin@example.com", "password": "secret"},
            )
        assert response.status_code == 403

    def test_login_missing_fields(self):
        """Missing username/password returns 422."""
        response = client.post("/auth/login", data={})
        assert response.status_code == 422

    def test_no_register_endpoint(self):
        """Public /auth/register should NOT exist (removed for security)."""
        response = client.post(
            "/auth/register",
            json={"name": "Hacker", "email": "h@h.com", "password": "pw", "role": "ADMIN"},
        )
        assert response.status_code == 404
