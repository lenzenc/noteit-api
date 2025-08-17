from fastapi import APIRouter

from noteit_api.api.v1.endpoints import health, upload

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(upload.router, tags=["upload"])