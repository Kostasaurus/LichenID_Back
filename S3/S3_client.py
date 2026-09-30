import asyncio
from contextlib import asynccontextmanager

from aiobotocore.session import get_session

from lichenid.core.settings import settings


class S3Client:
    def __init__(self):
        self.config = {
            "aws_access_key_id": settings.S3_settings.S3_access_key,
            "aws_secret_access_key": settings.S3_settings.S3_secret_key.get_secret_value(),
            "endpoint_url": settings.S3_settings.S3_url,
            "region_name": 'ru-3'
            # "signature_version": 's3v4'
        }
        self.bucket_name = settings.S3_settings.S3_bucket
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config, verify=False) as client:
            yield client


    async def upload_file(
            self,
            contents,
            key: str,
            content_type
    ) -> None:

        async with self.get_client() as client:

            await client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=contents,
                ContentType=content_type
            )

    async def get_object(self, object_key):
        async with self.get_client() as client:
            blob = await client.get_object(
                Bucket=self.bucket_name,
                Key=object_key,

            )
            return blob

    async def generate_url(
            self,
            key: str,
            expires_in: int = 3600
    ) -> str:
        async with self.get_client() as client:
            url = await client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': key
                },
                ExpiresIn=expires_in
            )
            return url





