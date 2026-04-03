from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated, List

from app.api.deps import require_role, get_current_active_user
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import user_service
from app.core.limiter import limiter

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201)
@limiter.limit("5/minute")
def create_user(
    request: Request,
    user_in: UserCreate,
    current_user: Annotated[dict, Depends(require_role(["ADMIN"]))],
):
    """Create a new user. ADMIN only. Max 5 per minute."""
    existing = user_service.get_user_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = user_service.create_user(user_in)
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return new_user


@router.get("/", response_model=List[UserResponse])
def list_users(
    current_user: Annotated[dict, Depends(require_role(["ADMIN"]))],
):
    """List all users. ADMIN only."""
    return user_service.get_all_users()


@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: Annotated[dict, Depends(get_current_active_user)],
):
    """Get the currently authenticated user's profile."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: str,
    current_user: Annotated[dict, Depends(require_role(["ADMIN"]))],
):
    """Get a user by ID. ADMIN only."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}/status", response_model=UserResponse)
def set_user_status(
    user_id: str,
    is_active: bool,
    current_user: Annotated[dict, Depends(require_role(["ADMIN"]))],
):
    """Activate or deactivate a user. ADMIN only."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated = user_service.set_user_active(user_id, is_active)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update user status")
    return updated
