import uuid
from typing import Optional

from sqlalchemy import insert, update, delete, func, select
from sqlalchemy.orm import selectinload

from src.models import tables
from src.services.repository.base import BaseRepository


class MessageRepo(BaseRepository[tables.Message]):
    table = tables.Message
