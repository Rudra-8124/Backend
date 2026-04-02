from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import user_service
from app.core.security import verify_password, create_access_token, settings
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_service.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user['id'])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate):
    print("Registering new user")
    user = user_service.get_user_by_email(user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = user_service.create_user(user_in)
    return new_user
