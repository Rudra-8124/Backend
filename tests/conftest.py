"""
conftest.py — Shared pytest fixtures for the Finance API test suite.

Uses TestClient with mocked Supabase calls so tests don't need a live DB.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# ── Provide dummy env vars before the app is imported ──────────────────────
import os
os.environ.setdefault("SUPABASE_URL", "https://fake.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "fake-key")
os.environ.setdefault("SECRET_KEY", "testsecretkey1234567890abcdef12")

# ── Patch the supabase client so no real HTTP is made ──────────────────────
mock_supabase = MagicMock()

with patch("app.db.supabase_client.create_client", return_value=mock_supabase):
    from app.main import app  # import after patch

client = TestClient(app)

from app.core.security import get_password_hash

# ── Sample data fixtures ────────────────────────────────────────────────────

TEST_PASSWORD_HASH = get_password_hash("secret")

ADMIN_USER = {
    "id": "11111111-1111-1111-1111-111111111111",
    "name": "Admin User",
    "email": "admin@example.com",
    "password": TEST_PASSWORD_HASH,
    "role": "ADMIN",
    "is_active": True,
    "created_at": "2024-01-01T00:00:00",
}

ANALYST_USER = {
    "id": "22222222-2222-2222-2222-222222222222",
    "name": "Analyst User",
    "email": "analyst@example.com",
    "password": TEST_PASSWORD_HASH,
    "role": "ANALYST",
    "is_active": True,
    "created_at": "2024-01-01T00:00:00",
}

VIEWER_USER = {
    "id": "33333333-3333-3333-3333-333333333333",
    "name": "Viewer User",
    "email": "viewer@example.com",
    "password": TEST_PASSWORD_HASH,
    "role": "VIEWER",
    "is_active": True,
    "created_at": "2024-01-01T00:00:00",
}

SAMPLE_RECORD = {
    "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "user_id": "11111111-1111-1111-1111-111111111111",
    "amount": 100.0,
    "type": "income",
    "category": "Salary",
    "date": "2024-06-01",
    "description": "Monthly salary",
    "created_at": "2024-06-01T10:00:00",
}


def _get_token_for_user(user: dict) -> str:
    """Helper: get a JWT by mocking the DB to return the given user."""
    from app.core.security import create_access_token
    from datetime import timedelta
    return create_access_token({"sub": user["id"]}, expires_delta=timedelta(minutes=30))


@pytest.fixture
def admin_token():
    with patch("app.services.user_service.fetch_data", return_value=[ADMIN_USER]):
        return _get_token_for_user(ADMIN_USER)


@pytest.fixture
def analyst_token():
    with patch("app.services.user_service.fetch_data", return_value=[ANALYST_USER]):
        return _get_token_for_user(ANALYST_USER)


@pytest.fixture
def viewer_token():
    with patch("app.services.user_service.fetch_data", return_value=[VIEWER_USER]):
        return _get_token_for_user(VIEWER_USER)
