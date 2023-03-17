from src.models.schemas.dialog import Dialog
from src.views.base import BaseView
from src.models.schemas import dialog


class DialogListResponse(BaseView):
    message: list[Dialog]
