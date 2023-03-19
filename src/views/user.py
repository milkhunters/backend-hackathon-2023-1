from src.views.base import BaseView
from src.models.schemas import User, UserSmall, UserMiddle


class UserBigResponse(BaseView):
    message: User


class UserMiddleResponse(BaseView):
    message: UserMiddle


class UserSmallResponse(BaseView):
    message: UserSmall


class UserSmallListResponse(BaseView):
    message: list[UserSmall]
