from src.views.base import BaseView
from src.models.schemas import User, UserSmall


class UserBigResponse(BaseView):
    message: User


class UserSmallResponse(BaseView):
    message: UserSmall
