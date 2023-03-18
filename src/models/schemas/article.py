import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    text: str

    class Config:
        orm_mode = True


class ArticleDelete(Article):
    id: uuid.UUID


class ArticleUpdate(BaseModel):
    title: str
    text: str
