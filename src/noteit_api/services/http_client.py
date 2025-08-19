import httpx
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from noteit_api.core.config import settings


class HTTPClientService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def proxy_get(self, url: str) -> StreamingResponse:
        """Proxy a GET request and return a streaming response"""
        try:
            # Use regular get() instead of stream() for simpler implementation
            response = await self.client.get(url)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Image processing failed: {response.reason_phrase}"
                )
            
            # Get content type from response headers
            content_type = response.headers.get("content-type", "image/jpeg")
            
            # Create streaming response from the content
            import io
            content_stream = io.BytesIO(response.content)
            
            return StreamingResponse(
                content_stream,
                media_type=content_type,
                headers={
                    "Content-Length": str(len(response.content)),
                    "Cache-Control": "public, max-age=3600"  # Cache for 1 hour
                }
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to proxy request: {str(e)}"
            )
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


http_client_service = HTTPClientService()