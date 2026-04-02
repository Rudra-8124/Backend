from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserModel(BaseModel):
    id: Optional[UUID] = None
    name: str
    email: str
    password: str
    role: str
    is_active: bool = True
    created_at: Optional[datetime] = None
