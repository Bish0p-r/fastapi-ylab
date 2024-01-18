from app.common.base.repository import BaseRepository
from app.models.menu import Menu


class MenuRepository(BaseRepository):
    model = Menu
