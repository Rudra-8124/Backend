from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.deps import require_role
from app.schemas.user import UserResponse
from app.services.user_service import user_service

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: Annotated[dict, Depends(require_role(["ADMIN", "ANALYST", "VIEWER"]))]):
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: str, current_user: Annotated[dict, Depends(require_role(["ADMIN"]))]):
    user = user_service.get_user_by_id(user_id)
    return user
