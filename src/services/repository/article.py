from src.models import tables
from src.services.repository.base import BaseRepository


class ArticleRepo(BaseRepository[tables.Article]):
    table = tables.Article

