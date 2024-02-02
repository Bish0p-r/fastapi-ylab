import pickle
from typing import Any

from redis import asyncio as aioredis

from app.config import settings


class CacheService:
    def __init__(self, ttl: int = settings.CACHE_TTL):
        self.ttl = ttl
        self.host = settings.REDIS_TEST_HOST if settings.MODE == 'TEST' else settings.REDIS_HOST
        self.port = settings.REDIS_PORT
        self.redis = aioredis.Redis(host=self.host, port=self.port)

    async def clear_cache(self, *patterns: str) -> None:
        keys = []
        for pattern in patterns:
            keys.extend(await self.redis.keys(pattern))
        if keys:
            await self.redis.delete(*keys)

    async def set_cache(self, key: str, value: Any) -> None:
        await self.redis.set(key, pickle.dumps(value), ex=self.ttl)

    async def get_cache(self, key: str) -> Any:
        cached_data = await self.redis.get(key)
        if cached_data is not None:
            return pickle.loads(cached_data)
