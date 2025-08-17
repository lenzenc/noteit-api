from fastapi import APIRouter

from noteit_api.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        message="NoteIt API is running successfully",
        version="0.1.0"
    )