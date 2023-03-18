from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory
from src.views import UserBigResponse
from src.views.banner import BannerResponse

router = APIRouter()


@router.get("/list", status_code=http_status.HTTP_200_OK, response_model=BannerResponse)
async def banner_list(service: ServiceFactory = Depends(get_services)):
    return BannerResponse(message=await service.banner.get_banners())


@router.post('/add', status_code=http_status.HTTP_204_NO_CONTENT)
async def banner_add(request: Request, response: Response, service: ServiceFactory = Depends(get_services)):
    pass

