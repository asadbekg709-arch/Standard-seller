import hashlib
import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)
_redis: Optional[aioredis.Redis] = None


async def get_redis() -> Optional[aioredis.Redis]:
    global _redis
    if _redis is None:
        try:
            settings = get_settings()
            _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
            await _redis.ping()
        except Exception as e:
            logger.warning(f"Redis unavailable, caching disabled: {e}")
            _redis = None
    return _redis


def make_cache_key(feature: str, data: dict) -> str:
    payload = json.dumps(data, sort_keys=True)
    digest = hashlib.md5(payload.encode()).hexdigest()
    return f"ai:{feature}:{digest}"


async def cache_get(key: str) -> Optional[Any]:
    client = await get_redis()
    if client is None:
        return None
    try:
        value = await client.get(key)
        return json.loads(value) if value else None
    except Exception as e:
        logger.warning(f"Cache get error: {e}")
        return None


async def cache_set(key: str, value: Any, ttl: int = 3600) -> None:
    client = await get_redis()
    if client is None:
        return
    try:
        await client.set(key, json.dumps(value), ex=ttl)
    except Exception as e:
        logger.warning(f"Cache set error: {e}")
