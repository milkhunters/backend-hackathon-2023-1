from src.models.schemas.article import Article, ArticleDelete
from src.views import BaseView


class ArticleListResponse(BaseView):
    message: list[Article]


class CreateArticleResponse(BaseView):
    message: Article


class UpdateArticleResponse(BaseView):
    message: Article


class DeleteArticleResponse(BaseView):
    message: ArticleDelete
