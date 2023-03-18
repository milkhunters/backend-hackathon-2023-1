import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Article(BaseModel):
    id: uuid.UUID
    title: str
    text: str
    create_at: datetime
    update_at: Optional[datetime]

    class Config:
        orm_mode = True


class CreateArticle(BaseModel):
    title: str
    text: str


class ArticleDelete(Article):
    id: uuid.UUID


class ArticleUpdate(BaseModel):
    title: str
    text: str
