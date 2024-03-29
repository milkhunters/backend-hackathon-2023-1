from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.services import ServiceFactory
from src.views.article import ArticleListResponse

router = APIRouter()


@router.get("/list", response_model=ArticleListResponse, status_code=http_status.HTTP_200_OK)
async def get_article_list_range(count: int, services: ServiceFactory = Depends(get_services)):
    return ArticleListResponse(message=await services.article.get_article_list_range(count))
