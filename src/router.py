from fastapi import APIRouter

from src.controllers import auth
from src.controllers import user
from src.controllers import admin
from src.controllers import stats
from src.controllers import dialog
from src.controllers import article
from src.controllers import file
from src.controllers import banner
from src.controllers import high_user


def reg_root_api_router(is_debug: bool) -> APIRouter:
    root_api_router = APIRouter(prefix="/api/v1" if is_debug else "")

    root_api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
    root_api_router.include_router(user.router, prefix="/user", tags=["User"])
    root_api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
    root_api_router.include_router(high_user.router, prefix="/high_user", tags=["HighUser"])
    root_api_router.include_router(stats.router, prefix="", tags=["Stats"])
    root_api_router.include_router(dialog.router, prefix="/dialog", tags=["Chat"])
    root_api_router.include_router(article.router, prefix="/article", tags=["Articles"])
    root_api_router.include_router(file.router, prefix="/file", tags=["Files"])
    root_api_router.include_router(banner.router, prefix="/banner", tags=["Banners"])

    return root_api_router
