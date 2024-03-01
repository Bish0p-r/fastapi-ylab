from abc import ABC, abstractmethod
from typing import Any

from app.config import settings


class AbstractCacheServices(ABC):
    @abstractmethod
    async def setup(self) -> None:
        ...

    @abstractmethod
    async def clear_cache(self, patterns: tuple[str, ...]) -> None:
        ...

    @abstractmethod
    async def clear_all_cache(self) -> None:
        ...

    @abstractmethod
    async def set_cache(self, key: str, value: Any, ex: int | None = settings.CACHE_TTL) -> None:
        ...

    @abstractmethod
    async def get_cache(self, key: str) -> Any:
        ...
