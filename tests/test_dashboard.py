"""
tests/test_dashboard.py  —  Tests for /dashboard endpoints
"""
from unittest.mock import patch, MagicMock
from tests.conftest import client, ADMIN_USER, ANALYST_USER, VIEWER_USER, SAMPLE_RECORD
from app.core.security import create_access_token
from datetime import timedelta


def _auth(user):
    token = create_access_token({"sub": user["id"]}, expires_delta=timedelta(minutes=30))
    return {"Authorization": f"Bearer {token}"}


def _mock_user(user):
    return patch("app.services.user_service.fetch_data", return_value=[user])


MOCK_RECORDS = [
    {**SAMPLE_RECORD, "amount": 1000.0, "type": "income", "category": "Salary"},
    {**SAMPLE_RECORD, "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "amount": 200.0, "type": "expense", "category": "Food"},
]


def _mock_supabase_records(records=None):
    if records is None:
        records = MOCK_RECORDS
    mock_sb = MagicMock()
    mock_sb.table.return_value.select.return_value.execute.return_value.data = records
    mock_sb.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value.data = records
    return patch("app.services.dashboard_service.supabase", mock_sb)


class TestDashboardSummary:
    def test_all_roles_can_access_summary(self):
        for user in [ADMIN_USER, ANALYST_USER, VIEWER_USER]:
            with _mock_user(user):
                with _mock_supabase_records():
                    resp = client.get("/dashboard/summary", headers=_auth(user))
            assert resp.status_code == 200

    def test_summary_structure(self):
        with _mock_user(ADMIN_USER):
            with _mock_supabase_records():
                resp = client.get("/dashboard/summary", headers=_auth(ADMIN_USER))
        data = resp.json()
        assert "total_income" in data
        assert "total_expense" in data
        assert "net_balance" in data
        assert data["total_income"] == 1000.0
        assert data["total_expense"] == 200.0
        assert data["net_balance"] == 800.0

    def test_unauthenticated_blocked(self):
        resp = client.get("/dashboard/summary")
        assert resp.status_code == 401


class TestCategorySummary:
    def test_category_summary_returns_dict(self):
        with _mock_user(ADMIN_USER):
            with _mock_supabase_records():
                resp = client.get("/dashboard/category-summary", headers=_auth(ADMIN_USER))
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert "Salary" in data
        assert "Food" in data

    def test_unauthenticated_blocked(self):
        resp = client.get("/dashboard/category-summary")
        assert resp.status_code == 401


class TestRecentTransactions:
    def test_recent_transactions_returns_list(self):
        with _mock_user(ADMIN_USER):
            with _mock_supabase_records():
                resp = client.get("/dashboard/recent-transactions", headers=_auth(ADMIN_USER))
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_empty_transactions(self):
        with _mock_user(ADMIN_USER):
            with _mock_supabase_records(records=[]):
                resp = client.get("/dashboard/recent-transactions", headers=_auth(ADMIN_USER))
        assert resp.status_code == 200
        assert resp.json() == []


class TestTrends:
    def test_trends_returns_dict(self):
        with _mock_user(ADMIN_USER):
            with _mock_supabase_records():
                resp = client.get("/dashboard/trends", headers=_auth(ADMIN_USER))
        assert resp.status_code == 200
        assert isinstance(resp.json(), dict)

    def test_unauthenticated_blocked(self):
        resp = client.get("/dashboard/trends")
        assert resp.status_code == 401
