from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    filename: str
    file_id: str
    file_size: int
    content_type: str
    imgproxy_url: str


class ImageProcessingOptions(BaseModel):
    width: int | None = None
    height: int | None = None
    quality: int = 85
    format: str = "webp"