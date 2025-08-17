import uuid
from io import BytesIO
from typing import Tuple

from minio import Minio
from minio.error import S3Error

from noteit_api.core.config import settings


class MinIOService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET_NAME):
                self.client.make_bucket(settings.MINIO_BUCKET_NAME)
        except S3Error as e:
            print(f"Error ensuring bucket exists: {e}")

    def upload_file(self, file_content: bytes, filename: str, content_type: str) -> Tuple[str, int]:
        file_id = f"{uuid.uuid4()}-{filename}"
        file_size = len(file_content)
        
        try:
            self.client.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=file_id,
                data=BytesIO(file_content),
                length=file_size,
                content_type=content_type
            )
            return file_id, file_size
        except S3Error as e:
            raise Exception(f"Failed to upload file: {e}")

    def delete_file(self, file_id: str) -> bool:
        try:
            self.client.remove_object(settings.MINIO_BUCKET_NAME, file_id)
            return True
        except S3Error:
            return False

    def file_exists(self, file_id: str) -> bool:
        try:
            self.client.stat_object(settings.MINIO_BUCKET_NAME, file_id)
            return True
        except S3Error:
            return False


minio_service = MinIOService()