import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory
from src.views import CreateArticleResponse, UpdateArticleResponse, DeleteArticleResponse

router = APIRouter()


@router.delete("/delete_user", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    await services.user.delete_user(user_id)


@router.post("/update_user", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(
        user_id: uuid.UUID,
        data: schemas.UserUpdateByAdmin,
        services: ServiceFactory = Depends(get_services)
):
    await services.user.update_user(user_id, data)


@router.post("/create_user", status_code=http_status.HTTP_201_CREATED)
async def create_user(user: schemas.UserSignUp, service: ServiceFactory = Depends(get_services)):
    await service.auth.create_user(user)


@router.post("/update_user/password", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user_password(
        user_id: uuid.UUID,
        password: str,
        service: ServiceFactory = Depends(get_services)
):
    await service.user.update_user_password(user_id, password)


@router.post("/article/create", response_model=CreateArticleResponse, status_code=http_status.HTTP_200_OK)
async def create_articles(article: schemas.CreateArticle, services: ServiceFactory = Depends(get_services)):
    return CreateArticleResponse(message=await services.article.create_article(article))


@router.post("/article/update", response_model=UpdateArticleResponse, status_code=http_status.HTTP_200_OK)
async def update_articles(services: ServiceFactory = Depends(get_services)):
    return UpdateArticleResponse(message=await services.article.update_article())


@router.delete("/article/delete", response_model=DeleteArticleResponse, status_code=http_status.HTTP_200_OK)
async def delete_article(article_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    return DeleteArticleResponse(message=await services.article.delete_article(article_id))
