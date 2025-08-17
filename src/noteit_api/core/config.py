import os
from typing import List

from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "NoteIt API")
    VERSION: str = os.getenv("VERSION", "0.1.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
    
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "images")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    
    IMGPROXY_URL: str = os.getenv("IMGPROXY_URL", "http://localhost:8080")
    IMGPROXY_KEY: str = os.getenv("IMGPROXY_KEY", "943b421c9eb07c830af81030552c86009268de4e532ba2ee2eab8247c6da0881")
    IMGPROXY_SALT: str = os.getenv("IMGPROXY_SALT", "520f986b998545b4785e0defbc4f3c1203f22de2374a3d53cb7a7fe9fea309c5")


settings = Settings()