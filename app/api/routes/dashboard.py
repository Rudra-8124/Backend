from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.deps import require_role
from app.services.dashboard_service import dashboard_service

router = APIRouter()

@router.get("/summary")
def get_summary(current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST", "VIEWER"]))]):
    return dashboard_service.get_summary()

@router.get("/category-summary")
def get_category_summary(current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST", "VIEWER"]))]):
    return dashboard_service.get_category_summary()

@router.get("/recent-transactions")
def get_recent_transactions(current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST", "VIEWER"]))]):
    return dashboard_service.get_recent_transactions()

@router.get("/trends")
def get_trends(current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST", "VIEWER"]))]):
    return dashboard_service.get_trends()
