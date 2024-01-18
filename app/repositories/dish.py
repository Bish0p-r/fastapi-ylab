from app.common.base.repository import BaseRepository
from app.models.dish import Dish


class DishRepository(BaseRepository):
    model = Dish
