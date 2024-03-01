import pickle
from typing import Any

from redis import asyncio as aioredis

from app.common.abstract.services.cache import AbstractCacheServices
from app.config import settings


class CacheService(AbstractCacheServices):
    def __init__(self, host: str = settings.REDIS_HOST, port: int = settings.REDIS_PORT) -> None:
        self.host = host
        self.port = port

    async def setup(self) -> None:
        self.redis = aioredis.Redis(host=self.host, port=self.port)

    async def clear_cache(self, patterns: tuple[str, ...]) -> None:
        keys = {key for pattern in patterns for key in await self.redis.keys(pattern)}
        if keys:
            await self.redis.delete(*keys)

    async def clear_all_cache(self) -> None:
        await self.redis.flushall()

    async def set_cache(self, key: str, value: Any, ex: int | None = settings.CACHE_TTL) -> None:
        await self.redis.set(key, pickle.dumps(value), ex=ex)

    async def get_cache(self, key: str) -> Any:
        cached_data = await self.redis.get(key)
        if cached_data is not None:
            return pickle.loads(cached_data)


cache_service = CacheService()
