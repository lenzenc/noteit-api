from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from noteit_api.schemas.upload import ImageProcessingOptions
from noteit_api.services.http_client import http_client_service
from noteit_api.services.imgproxy import imgproxy_service

router = APIRouter()


@router.get("/{file_id}")
async def get_image(
    file_id: str,
    width: Optional[int] = Query(None, description="Image width in pixels"),
    height: Optional[int] = Query(None, description="Image height in pixels"),
    quality: int = Query(85, ge=1, le=100, description="Image quality (1-100)"),
    format: str = Query("webp", description="Output format (webp, jpeg, png)")
) -> StreamingResponse:
    """Get an image with optional processing parameters"""
    
    try:
        # Create processing options if any parameters are provided
        if width or height or quality != 85 or format != "webp":
            options = ImageProcessingOptions(
                width=width,
                height=height,
                quality=quality,
                format=format
            )
            imgproxy_url = imgproxy_service.generate_url(file_id, options)
        else:
            # Use raw URL for unprocessed images
            imgproxy_url = imgproxy_service.generate_raw_url(file_id)
        
        # Proxy the request to ImgProxy
        return await http_client_service.proxy_get(imgproxy_url)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve image: {str(e)}"
        )