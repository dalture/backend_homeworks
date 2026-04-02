from src.adapters.storage.base import StorageAdapter
from src.adapters.storage.s3 import S3StorageAdapter

from src.core.config import settings


async def get_storage() -> StorageAdapter:
    return S3StorageAdapter(
        bucket=settings.s3_bucket_name,
        url=settings.s3_endpoint_url,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        region=settings.s3_region,
    )