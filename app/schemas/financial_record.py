from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class FinancialRecordBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: str # 'income' or 'expense'
    category: str
    date: str
    description: Optional[str] = None
    
    @validator('type')
    def check_type(cls, v):
        if v not in ['income', 'expense']:
            raise ValueError("Type must be either 'income' or 'expense'")
        return v

class FinancialRecordCreate(FinancialRecordBase):
    pass

class FinancialRecordUpdate(FinancialRecordBase):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None

class FinancialRecordResponse(FinancialRecordBase):
    id: UUID
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
