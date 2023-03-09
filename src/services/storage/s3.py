import random
from contextlib import AsyncExitStack
from typing import Optional, Union, IO

from .base import AbstractStorage, File, ContentType

from aiobotocore.session import AioSession


class S3Storage(AbstractStorage):  # Обернуть в app -> di

    def __init__(
            self,
            endpoint_url: str,
            region_name: str,
            aws_access_key_id: str,
            aws_secret_access_key: str,
            bucket: str,
            service_name: str = "s3"
    ):
        self._bucket = bucket
        self._service_name = service_name
        self._endpoint_url = endpoint_url

        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._region_name = region_name

        self._exit_stack = AsyncExitStack()
        self._client = None

    async def __aenter__(self):
        session = AioSession()
        self._client = await self._exit_stack.enter_async_context(
            session.create_client(
                aws_secret_access_key=self._aws_secret_access_key,
                aws_access_key_id=self._aws_access_key_id,
                region_name=self._region_name,

                service_name=self._service_name,
                endpoint_url=self._endpoint_url,
                use_ssl=False
            )
        )
        return self

    async def get(self, path_to_file: str) -> Optional[File]:
        try:
            response = await self._client.get_object(Bucket=self._bucket, Key=path_to_file)
        except Exception:
            # TODO: отловить правильно ошибку: найти botocore.errorfactory.NoSuchKey класс
            return None

        async with response['Body'] as stream:
            return File(
                id=path_to_file.split("/")[-1],
                name=response['Metadata']['filename'],
                content_type=ContentType(response['Metadata']['content_type']),
                bytes=await stream.read(),
                owner_id=int(response['Metadata']['owner_id']),
                size=int(response['ContentLength'])
            )

    async def save(self, path_to_file: str, content_type: ContentType, file: Union[bytes, IO], owner_id: int) -> str:
        """
        path_to_file: str - путь к файлу в хранилище, пример: "user/1/1.jpg"

        """
        file_id = f"{owner_id}_{random.randint(100000000, 999999999)}"
        await self._client.put_object(
            Bucket=self._bucket,
            Body=file,
            Key=path_to_file,
            Metadata={
                "filename": path_to_file.split("/")[-1],
                "owner_id": str(owner_id),
                "content_type": content_type.value
            }
        )
        return file_id

    async def info(self, path_to_file: str) -> dict:
        response = await self._client.get_object(Bucket=self._bucket, Key=path_to_file)
        return {
            "filename": response['Metadata']['filename'],
            "owner_id": response['Metadata']['owner_id'],
            "content_type": ContentType(response['Metadata']['content_type']),
            "size": int(response['ContentLength']),
        }

    async def delete(self, path_to_file) -> None:
        await self._client.delete_object(Bucket=self._bucket, Key=path_to_file)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)
