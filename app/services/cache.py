import pickle
from typing import Any

from redis import asyncio as aioredis

from app.config import settings


class CacheService:
    def __init__(
        self, ttl: int = settings.CACHE_TTL, host: str = settings.REDIS_HOST, port: int = settings.REDIS_PORT
    ) -> None:
        self.ttl = ttl
        self.host = host
        self.port = port

    async def setup(self) -> None:
        self.redis = aioredis.Redis(host=self.host, port=self.port)

    async def clear_cache(self, patterns: tuple[str, ...]) -> None:
        keys = {key for pattern in patterns for key in await self.redis.keys(pattern)}
        if keys:
            await self.redis.delete(*keys)

    async def set_cache(self, key: str, value: Any) -> None:
        await self.redis.set(key, pickle.dumps(value), ex=self.ttl)

    async def get_cache(self, key: str) -> Any:
        cached_data = await self.redis.get(key)
        if cached_data is not None:
            return pickle.loads(cached_data)


cache_service = CacheService()
