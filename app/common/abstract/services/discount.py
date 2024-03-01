from abc import ABC, abstractmethod

from app.models.dish import Dish


class AbstractDiscountServices(ABC):
    @abstractmethod
    async def set_discount(self, *dishes: Dish) -> None:
        ...
