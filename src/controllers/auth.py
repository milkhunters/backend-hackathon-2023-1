from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory
from src.views import UserBigResponse

router = APIRouter()


@router.put("/signUp", status_code=http_status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserSignUp, service: ServiceFactory = Depends(get_services)):
    await service.auth.create_user(user)


@router.post("/signIn", status_code=http_status.HTTP_200_OK, response_model=UserBigResponse)
async def sign_in(user: schemas.UserSignIn, response: Response, service: ServiceFactory = Depends(get_services)):
    return UserBigResponse(message=await service.auth.authenticate(user.username, user.password, response))


@router.post('/logout', status_code=http_status.HTTP_204_NO_CONTENT)
async def logout_controller(request: Request, response: Response, service: ServiceFactory = Depends(get_services)):
    await service.auth.logout(request, response)


@router.post('/refresh_tokens', status_code=http_status.HTTP_204_NO_CONTENT)
async def refresh(request: Request, response: Response, service: ServiceFactory = Depends(get_services)):
    await service.auth.refresh_tokens(request, response)
