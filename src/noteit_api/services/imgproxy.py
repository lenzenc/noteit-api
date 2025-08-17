import base64
import hashlib
import hmac
from urllib.parse import quote

from noteit_api.core.config import settings
from noteit_api.schemas.upload import ImageProcessingOptions


class ImgProxyService:
    def __init__(self):
        self.base_url = settings.IMGPROXY_URL
        self.key = bytes.fromhex(settings.IMGPROXY_KEY)
        self.salt = bytes.fromhex(settings.IMGPROXY_SALT)

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

        # Build processing path
        processing_path = f"/resize:{resize_type}:{width}:{height}/quality:{quality}/{encoded_source}.{format_ext}"

        # Generate signature
        signature = self._generate_signature(processing_path)

        # Return the complete ImgProxy URL
        return f"{self.base_url}/{signature}{processing_path}"

    def generate_raw_url(self, file_id: str) -> str:
        source_url = f"s3://{settings.MINIO_BUCKET_NAME}/{file_id}"
        encoded_source = base64.urlsafe_b64encode(source_url.encode()).decode().rstrip('=')
        
        processing_path = f"/{encoded_source}"
        signature = self._generate_signature(processing_path)
        
        return f"{self.base_url}/{signature}{processing_path}"

    def _generate_signature(self, path: str) -> str:
        digest = hmac.new(self.key, path.encode() + self.salt, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(digest).decode().rstrip('=')


imgproxy_service = ImgProxyService()