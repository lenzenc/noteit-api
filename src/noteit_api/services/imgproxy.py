import base64

from noteit_api.core.config import settings
from noteit_api.schemas.upload import ImageProcessingOptions


class ImgProxyService:
    def __init__(self):
        self.base_url = settings.IMGPROXY_URL

    def generate_url(self, file_id: str, options: ImageProcessingOptions | None = None) -> str:
        if not options:
            options = ImageProcessingOptions()

        # Build the processing options string
        resize_type = "fit"
        width = options.width or 0
        height = options.height or 0
        quality = options.quality
        format_ext = options.format

        # Create the source URL for MinIO
        source_url = f"s3://{settings.MINIO_BUCKET_NAME}/{file_id}"
        encoded_source = base64.urlsafe_b64encode(source_url.encode()).decode().rstrip('=')

        # Build processing path with /insecure/ for unsigned URLs
        processing_path = f"/insecure/resize:{resize_type}:{width}:{height}/quality:{quality}/{encoded_source}.{format_ext}"

        # Return the complete ImgProxy URL (unsigned)
        return f"{self.base_url}{processing_path}"

    def generate_raw_url(self, file_id: str) -> str:
        source_url = f"s3://{settings.MINIO_BUCKET_NAME}/{file_id}"
        encoded_source = base64.urlsafe_b64encode(source_url.encode()).decode().rstrip('=')
        
        # Extract file extension from file_id for ImgProxy format
        file_ext = file_id.split('.')[-1] if '.' in file_id else 'jpg'
        processing_path = f"/insecure/{encoded_source}.{file_ext}"
        
        return f"{self.base_url}{processing_path}"



imgproxy_service = ImgProxyService()