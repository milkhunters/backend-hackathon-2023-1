import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory
from src.views.article import ArticleListResponse, CreateArticleResponse, UpdateArticleResponse, DeleteArticleResponse, \
    ArticleResponse

router = APIRouter()


@router.get("/articles", response_model=ArticleListResponse, status_code=http_status.HTTP_200_OK)
async def get_article_list_range(count: int, services: ServiceFactory = Depends(get_services)):
    return ArticleListResponse(message=await services.article.get_article_list_range(count))
