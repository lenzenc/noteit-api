from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from noteit_api.api.v1.router import api_router
from noteit_api.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A note-taking API with image storage capabilities",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)