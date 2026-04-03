"""
tests/test_financial_records.py  —  Tests for /financial-records endpoints
"""
import pytest
from unittest.mock import patch
from tests.conftest import client, ADMIN_USER, ANALYST_USER, VIEWER_USER, SAMPLE_RECORD
from app.core.security import create_access_token
from datetime import timedelta


def _auth(user):
    token = create_access_token({"sub": user["id"]}, expires_delta=timedelta(minutes=30))
    return {"Authorization": f"Bearer {token}"}


def _mock_user(user):
    return patch("app.services.user_service.fetch_data", return_value=[user])


VALID_RECORD_PAYLOAD = {
    "amount": 500.0,
    "type": "income",
    "category": "Salary",
    "date": "2024-06-15",
    "description": "June salary",
}


class TestCreateRecord:
    def test_admin_can_create(self):
        with _mock_user(ADMIN_USER):
            with patch("app.services.financial_service.insert_data", return_value=SAMPLE_RECORD):
                resp = client.post("/financial-records/", json=VALID_RECORD_PAYLOAD, headers=_auth(ADMIN_USER))
        assert resp.status_code == 201

    def test_analyst_can_create(self):
        with _mock_user(ANALYST_USER):
            with patch("app.services.financial_service.insert_data", return_value=SAMPLE_RECORD):
                resp = client.post("/financial-records/", json=VALID_RECORD_PAYLOAD, headers=_auth(ANALYST_USER))
        assert resp.status_code == 201

    def test_viewer_cannot_create(self):
        with _mock_user(VIEWER_USER):
            resp = client.post("/financial-records/", json=VALID_RECORD_PAYLOAD, headers=_auth(VIEWER_USER))
        assert resp.status_code == 403

    def test_unauthenticated_cannot_create(self):
        resp = client.post("/financial-records/", json=VALID_RECORD_PAYLOAD)
        assert resp.status_code == 401

    def test_negative_amount_rejected(self):
        with _mock_user(ADMIN_USER):
            payload = {**VALID_RECORD_PAYLOAD, "amount": -100}
            resp = client.post("/financial-records/", json=payload, headers=_auth(ADMIN_USER))
        assert resp.status_code == 422

    def test_zero_amount_rejected(self):
        with _mock_user(ADMIN_USER):
            payload = {**VALID_RECORD_PAYLOAD, "amount": 0}
            resp = client.post("/financial-records/", json=payload, headers=_auth(ADMIN_USER))
        assert resp.status_code == 422

    def test_invalid_type_rejected(self):
        with _mock_user(ADMIN_USER):
            payload = {**VALID_RECORD_PAYLOAD, "type": "donation"}
            resp = client.post("/financial-records/", json=payload, headers=_auth(ADMIN_USER))
        assert resp.status_code == 422

    def test_missing_required_field(self):
        with _mock_user(ADMIN_USER):
            payload = {"amount": 100.0}  # missing type, category, date
            resp = client.post("/financial-records/", json=payload, headers=_auth(ADMIN_USER))
        assert resp.status_code == 422


class TestGetRecords:
    def test_all_roles_can_read(self):
        for user in [ADMIN_USER, ANALYST_USER, VIEWER_USER]:
            with _mock_user(user):
                with patch("app.db.supabase_client.supabase") as mock_sb:
                    mock_sb.table.return_value.select.return_value.execute.return_value.data = [SAMPLE_RECORD]
                    resp = client.get("/financial-records/", headers=_auth(user))
            assert resp.status_code == 200

    def test_filter_by_type(self):
        with _mock_user(ADMIN_USER):
            with patch("app.db.supabase_client.supabase") as mock_sb:
                chain = mock_sb.table.return_value.select.return_value
                chain.eq.return_value = chain
                chain.execute.return_value.data = [SAMPLE_RECORD]
                resp = client.get("/financial-records/?type=income", headers=_auth(ADMIN_USER))
        assert resp.status_code == 200

    def test_unauthenticated_cannot_read(self):
        resp = client.get("/financial-records/")
        assert resp.status_code == 401


class TestUpdateRecord:
    def test_analyst_can_update(self):
        with _mock_user(ANALYST_USER):
            with patch("app.services.financial_service.fetch_data", return_value=[SAMPLE_RECORD]):
                with patch("app.services.financial_service.update_data", return_value=SAMPLE_RECORD):
                    resp = client.put(
                        f"/financial-records/{SAMPLE_RECORD['id']}",
                        json={"amount": 200.0},
                        headers=_auth(ANALYST_USER),
                    )
        assert resp.status_code == 200

    def test_viewer_cannot_update(self):
        with _mock_user(VIEWER_USER):
            resp = client.put(
                f"/financial-records/{SAMPLE_RECORD['id']}",
                json={"amount": 200.0},
                headers=_auth(VIEWER_USER),
            )
        assert resp.status_code == 403

    def test_update_nonexistent_record(self):
        with _mock_user(ADMIN_USER):
            with patch("app.services.financial_service.fetch_data", return_value=[]):
                resp = client.put(
                    "/financial-records/nonexistent-id",
                    json={"amount": 100.0},
                    headers=_auth(ADMIN_USER),
                )
        assert resp.status_code == 404

    def test_partial_update_without_type(self):
        """PATCH with only 'amount' — type field should not trigger validator error."""
        with _mock_user(ADMIN_USER):
            with patch("app.services.financial_service.fetch_data", return_value=[SAMPLE_RECORD]):
                with patch("app.services.financial_service.update_data", return_value=SAMPLE_RECORD):
                    resp = client.put(
                        f"/financial-records/{SAMPLE_RECORD['id']}",
                        json={"amount": 999.0},  # omitting 'type'
                        headers=_auth(ADMIN_USER),
                    )
        assert resp.status_code == 200


class TestDeleteRecord:
    def test_admin_can_delete(self):
        with _mock_user(ADMIN_USER):
            with patch("app.services.financial_service.fetch_data", return_value=[SAMPLE_RECORD]):
                with patch("app.services.financial_service.delete_data", return_value=SAMPLE_RECORD):
                    resp = client.delete(
                        f"/financial-records/{SAMPLE_RECORD['id']}",
                        headers=_auth(ADMIN_USER),
                    )
        assert resp.status_code == 200

    def test_analyst_cannot_delete(self):
        with _mock_user(ANALYST_USER):
            resp = client.delete(
                f"/financial-records/{SAMPLE_RECORD['id']}",
                headers=_auth(ANALYST_USER),
            )
        assert resp.status_code == 403

    def test_delete_nonexistent_returns_404(self):
        with _mock_user(ADMIN_USER):
            with patch("app.services.financial_service.fetch_data", return_value=[]):
                resp = client.delete(
                    "/financial-records/nonexistent",
                    headers=_auth(ADMIN_USER),
                )
        assert resp.status_code == 404
