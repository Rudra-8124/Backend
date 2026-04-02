from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Annotated, List, Optional
from uuid import UUID

from app.api.deps import require_role
from app.schemas.financial_record import FinancialRecordCreate, FinancialRecordResponse, FinancialRecordUpdate
from app.services.financial_service import financial_service

router = APIRouter()

@router.post("/", response_model=FinancialRecordResponse)
def create_record(
    record_in: FinancialRecordCreate, 
    current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST"]))]
):
    record = financial_service.create_record(current_user['id'], record_in)
    return record

@router.get("/", response_model=List[dict]) # Just dict to avoid mapping error
def read_records(
    current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST", "VIEWER"]))],
    type: Optional[str] = Query(None, description="income or expense"),
    category: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    records = financial_service.get_records(type=type, category=category, start_date=start_date, end_date=end_date)
    return records

@router.put("/{record_id}", response_model=dict)
def update_record(
    record_id: str,
    record_in: FinancialRecordUpdate,
    current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST"]))]
):
    record = financial_service.update_record(record_id, record_in)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.delete("/{record_id}")
def delete_record(
    record_id: str,
    current_user: Annotated[dict, Depends(require_role(["ADMIN"]))]
):
    deleted = financial_service.delete_record(record_id)
    return {"message": "Record deleted successfully"}
