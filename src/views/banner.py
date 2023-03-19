from src.models.schemas.banner import Banner
from src.views.base import BaseView


class BannerResponse(BaseView):
    message: list[Banner]


class BannerAddResponse(BaseView):
    message: Banner
