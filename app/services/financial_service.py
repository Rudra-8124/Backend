from app.schemas.financial_record import FinancialRecordCreate, FinancialRecordUpdate
import uuid

records_db = []

class FinancialService:
    def create_record(self, user_id: str, record_in: FinancialRecordCreate):
        data = record_in.dict()
        data['id'] = str(uuid.uuid4())
        data['user_id'] = user_id
        
        records_db.append(data)
        return data

    def get_records(self, type: str = None, category: str = None, start_date: str = None, end_date: str = None):
        res = records_db
        if type: res = [r for r in res if r['type'] == type]
        if category: res = [r for r in res if r['category'] == category]
        return res

    def update_record(self, record_id: str, record_in: FinancialRecordUpdate):
        return None

    def delete_record(self, record_id: str):
        return None

financial_service = FinancialService()
