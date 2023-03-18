from src.models import tables
from src.services.repository.base import BaseRepository


class BannerRepo(BaseRepository[tables.Banner]):
    table = tables.Banner

