from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Annotated, List, Optional

from app.api.deps import require_role
from app.schemas.financial_record import (
    FinancialRecordCreate,
    FinancialRecordResponse,
    FinancialRecordUpdate,
)
from app.services.financial_service import financial_service

router = APIRouter()


@router.post("/", response_model=FinancialRecordResponse, status_code=201)
def create_record(
    record_in: FinancialRecordCreate,
    current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST"]))],
):
    """Create a financial record. ADMIN and ANALYST only."""
    record = financial_service.create_record(current_user['id'], record_in)
    if not record:
        raise HTTPException(status_code=500, detail="Failed to create record")
    return record


@router.get("/", response_model=List[FinancialRecordResponse])
def read_records(
    current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST", "VIEWER"]))],
    type: Optional[str] = Query(None, description="Filter by type: 'income' or 'expense'"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[str] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date filter (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search term in description or category"),
    skip: int = Query(0, ge=0, description="Number of records to skip (for pagination)"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of records to return")
):
    """Get all financial records with optional filters, pagination, and text search. All roles."""
    records = financial_service.get_records(
        type=type, category=category, start_date=start_date, end_date=end_date,
        search=search, skip=skip, limit=limit
    )
    return records


@router.get("/{record_id}", response_model=FinancialRecordResponse)
def read_record(
    record_id: str,
    current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST", "VIEWER"]))],
):
    """Get a single financial record by ID. All roles."""
    record = financial_service.get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.put("/{record_id}", response_model=FinancialRecordResponse)
def update_record(
    record_id: str,
    record_in: FinancialRecordUpdate,
    current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST"]))],
):
    """Update a financial record. ADMIN and ANALYST only."""
    record = financial_service.get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    updated = financial_service.update_record(record_id, record_in)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update record")
    return updated


@router.delete("/{record_id}", status_code=200)
def delete_record(
    record_id: str,
    current_user: Annotated[dict, Depends(require_role(["ADMIN"]))],
):
    """Delete a financial record. ADMIN only."""
    record = financial_service.get_record_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    financial_service.delete_record(record_id)
    return {"message": "Record deleted successfully"}
