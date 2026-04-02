from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, user, financial_record, dashboard
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json",
    description="Backend for Finance Data Processing and Access Control System API",
    version="1.0.0"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(financial_record.router, prefix="/financial-records", tags=["financial-records"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Finance Data Processing API"}
