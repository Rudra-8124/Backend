from app.schemas.financial_record import FinancialRecordCreate, FinancialRecordUpdate
from app.db.supabase_client import insert_data, fetch_data, update_data, delete_data
import uuid
from datetime import datetime


class FinancialService:
    TABLE = "financial_records"

    def create_record(self, user_id: str, record_in: FinancialRecordCreate):
        data = record_in.model_dump()
        data['id'] = str(uuid.uuid4())
        data['user_id'] = user_id
        data['created_at'] = datetime.utcnow().isoformat()
        inserted = insert_data(self.TABLE, data)
        return inserted if inserted else None

    def get_records(
        self,
        type: str = None,
        category: str = None,
        start_date: str = None,
        end_date: str = None,
    ):
        from app.db.supabase_client import supabase

        query = supabase.table(self.TABLE).select("*")

        if type:
            query = query.eq("type", type)
        if category:
            query = query.eq("category", category)
        if start_date:
            query = query.gte("date", start_date)
        if end_date:
            query = query.lte("date", end_date)

        response = query.execute()
        return response.data

    def get_record_by_id(self, record_id: str):
        records = fetch_data(self.TABLE, {"id": record_id})
        return records[0] if records else None

    def update_record(self, record_id: str, record_in: FinancialRecordUpdate):
        # Only send fields that were actually provided (not None)
        data = {k: v for k, v in record_in.model_dump().items() if v is not None}
        if not data:
            return self.get_record_by_id(record_id)
        updated = update_data(self.TABLE, record_id, data)
        return updated if updated else None

    def delete_record(self, record_id: str):
        deleted = delete_data(self.TABLE, record_id)
        return deleted


financial_service = FinancialService()
