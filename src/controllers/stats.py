from fastapi import APIRouter
from fastapi.requests import Request
from fastapi import status as http_status


router = APIRouter()


@router.get("/version", response_model=dict, status_code=http_status.HTTP_200_OK)
async def version(request: Request, details: bool = False):
    info = {
        "version": request.app.state.config.BASE.VERSION,
    }
    if details:
        info.update(
            {
                "name": None,
                "build": None,
                "build_date": None,
                "branch": None,
                "commit_hash": None,
            }
        )
    return info


@router.get("/test_redis", response_model=dict, status_code=http_status.HTTP_200_OK)
async def test_redis(request: Request):
    return {
        "Redis": await request.app.state.redis.ping(),
    }
