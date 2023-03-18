from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.services import ServiceFactory
from src.views.article import ArticleListResponse, CreateArticleResponse, UpdateArticleResponse, DeleteArticleResponse

router = APIRouter()


@router.get("/list", response_model=ArticleListResponse, status_code=http_status.HTTP_200_OK)
async def get_article_list(count: Optional[int], services: ServiceFactory = Depends(get_services)):
    pass


@router.post("/list/admin/create", response_model=CreateArticleResponse, status_code=http_status.HTTP_200_OK)
async def create_article(services: ServiceFactory = Depends(get_services)):
    pass


@router.put("/list/admin/update", response_model=UpdateArticleResponse, status_code=http_status.HTTP_200_OK)
async def update_article(services: ServiceFactory = Depends(get_services)):
    pass


@router.delete("/list/admin/delete", response_model=DeleteArticleResponse, status_code=http_status.HTTP_200_OK)
async def delete_article(services: ServiceFactory = Depends(get_services)):
    pass
