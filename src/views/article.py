import uuid

from src.models.schemas.article import Article, ArticleDelete, CreateArticle
from src.views import BaseView


class ArticleListResponse(BaseView):
    message: list[Article]


class ArticleResponse(BaseView):
    message: Article


class CreateArticleResponse(BaseView):
    message: uuid.UUID


class UpdateArticleResponse(BaseView):
    message: Article


class DeleteArticleResponse(BaseView):
    message: ArticleDelete
