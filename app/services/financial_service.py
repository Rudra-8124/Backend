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
        search: str = None,
        skip: int = 0,
        limit: int = 100
    ):
        from app.db.supabase_client import supabase

        query = supabase.table(self.TABLE).select("*").eq("is_deleted", False)

        if type:
            query = query.eq("type", type)
        if category:
            query = query.eq("category", category)
        if start_date:
            query = query.gte("date", start_date)
        if end_date:
            query = query.lte("date", end_date)
        if search:
            # Using Supabase ilike for case-insensitive search
            query = query.ilike("description", f"%{search}%")

        # Add pagination
        query = query.range(skip, skip + limit - 1)

        response = query.execute()
        return response.data

    def get_record_by_id(self, record_id: str):
        from app.db.supabase_client import supabase
        response = supabase.table(self.TABLE).select("*").eq("id", record_id).eq("is_deleted", False).execute()
        return response.data[0] if response.data else None

    def update_record(self, record_id: str, record_in: FinancialRecordUpdate):
        # Only send fields that were actually provided (not None)
        data = {k: v for k, v in record_in.model_dump().items() if v is not None}
        if not data:
            return self.get_record_by_id(record_id)
        from app.db.supabase_client import supabase
        response = supabase.table(self.TABLE).update(data).eq("id", record_id).eq("is_deleted", False).execute()
        return response.data[0] if response.data else None

    def delete_record(self, record_id: str):
        # Soft delete mechanism
        from app.db.supabase_client import supabase
        response = supabase.table(self.TABLE).update({"is_deleted": True}).eq("id", record_id).execute()
        return response.data[0] if response.data else None


financial_service = FinancialService()
