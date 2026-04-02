from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class FinancialRecordModel(BaseModel):
    id: Optional[UUID] = None
    user_id: str
    amount: float
    type: str # 'income' or 'expense'
    category: str
    date: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
