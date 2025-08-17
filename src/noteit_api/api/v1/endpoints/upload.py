from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from noteit_api.schemas.upload import UploadResponse
from noteit_api.services.imgproxy import imgproxy_service
from noteit_api.services.storage import minio_service

router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png", 
    "image/webp",
    "image/gif"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)) -> UploadResponse:
    # Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_CONTENT_TYPES)}"
        )
    
    # Read file content
    file_content = await file.read()
    
    # Validate file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024 * 1024)}MB"
        )
    
    # Validate file is not empty
    if len(file_content) == 0:
        raise HTTPException(
            status_code=400,
            detail="File is empty"
        )
    
    try:
        # Upload to MinIO
        file_id, file_size = minio_service.upload_file(
            file_content=file_content,
            filename=file.filename or "unnamed",
            content_type=file.content_type or "application/octet-stream"
        )
        
        # Generate ImgProxy URL
        imgproxy_url = imgproxy_service.generate_raw_url(file_id)
        
        return UploadResponse(
            message="File uploaded successfully",
            filename=file.filename or "unnamed",
            file_id=file_id,
            file_size=file_size,
            content_type=file.content_type or "application/octet-stream",
            imgproxy_url=imgproxy_url
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )