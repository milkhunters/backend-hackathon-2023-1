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


@router.get("/get_article", response_model=ArticleResponse, status_code=http_status.HTTP_200_OK)
async def get_article(article_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return ArticleResponse(message=await services.article.get_article(article_id))


@router.get("/list", response_model=ArticleListResponse, status_code=http_status.HTTP_200_OK)
async def get_article_list_range(count: int, services: ServiceFactory = Depends(get_services)):
    return ArticleListResponse(message=await services.article.get_article_list_range(count))


@router.post("/list/admin/create", response_model=CreateArticleResponse, status_code=http_status.HTTP_200_OK)
async def create_article(article: schemas.Article, services: ServiceFactory = Depends(get_services)):
    return CreateArticleResponse(message=await services.article.create_article(article))


"""
@router.put("/list/admin/update", response_model=UpdateArticleResponse, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_article(services: ServiceFactory = Depends(get_services)):
    return UpdateArticleResponse(message=await services.article.update_article())
"""


@router.delete("/list/admin/delete", response_model=DeleteArticleResponse, status_code=http_status.HTTP_200_OK)
async def delete_article(article_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return DeleteArticleResponse(message=await services.article.delete_article(article_id))
