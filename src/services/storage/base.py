import dataclasses
import uuid
from enum import Enum, unique
from abc import ABC, abstractmethod
from typing import Optional, Union, IO, Any


@dataclasses.dataclass
class File:
    id: uuid.UUID
    title: str
    content_type: Any
    size: Optional[int]
    bytes: Optional[Any]
    owner_id: uuid.UUID


class AbstractStorage(ABC):
    """Abstract storage class"""

    @abstractmethod
    async def __aenter__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def __aexit__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get(self, file_id: uuid.UUID, load_bytes: bool = False) -> Optional[File]:
        """
        Получить файл из хранилища
        :param file_id:
        :param load_bytes:
        :return:
        """
        pass

    @abstractmethod
    async def save(self, file_id: uuid.UUID, title: str, content_type: Any, file: Union[bytes, IO], owner_id: int):
        """
        Сохранить файл в хранилище
        :param owner_id:
        :param file:
        :param content_type: тип файла
        :param title: имя файла
        :param file_id
        """
        pass

    @abstractmethod
    async def delete(self, file_id: uuid.UUID) -> None:
        """
        Удалить файл из хранилища
        :param file_id:
        :return:
        """
        pass
