from fastapi import APIRouter
from api.schemas.response import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def root():
    return {"status": "ok", "message": "Opta Graph API is running"}

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy", "message": "API is operational"}