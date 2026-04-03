from pydantic import BaseModel, field_validator, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class FinancialRecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="Must be a positive number")
    type: str  # 'income' or 'expense'
    category: str
    date: str  # Expected format: YYYY-MM-DD
    description: Optional[str] = None
    is_deleted: bool = False

    @field_validator('type')
    @classmethod
    def check_type(cls, v):
        if v not in ('income', 'expense'):
            raise ValueError("type must be 'income' or 'expense'")
        return v


class FinancialRecordCreate(FinancialRecordBase):
    pass


class FinancialRecordUpdate(BaseModel):
    """All fields optional for partial updates."""
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None

    @field_validator('type')
    @classmethod
    def check_type(cls, v):
        # Allow None (field not provided); only validate when a value is given
        if v is not None and v not in ('income', 'expense'):
            raise ValueError("type must be 'income' or 'expense'")
        return v


class FinancialRecordResponse(FinancialRecordBase):
    id: UUID
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True
