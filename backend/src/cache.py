"""
Caching layer for frequently accessed data.
Provides Redis and in-memory caching with TTL support.
"""

import json
import logging
from typing import Any, Optional
import time

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from .config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class Cache:
    """Unified caching interface supporting Redis and in-memory fallback."""

    def __init__(self):
        self._memory_cache = {}
        self._redis_client = None

        if REDIS_AVAILABLE and settings.redis_url:
            try:
                self._redis_client = redis.from_url(settings.redis_url)
                self._redis_client.ping()  # Test connection
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.warning(f"Redis connection failed, falling back to memory cache: {e}")
                self._redis_client = None
        else:
            logger.info("Using in-memory cache")

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            if self._redis_client:
                value = self._redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Check memory cache with TTL
                if key in self._memory_cache:
                    value, expiry = self._memory_cache[key]
                    if expiry is None or time.time() < expiry:
                        return value
                    else:
                        # Expired, remove it
                        del self._memory_cache[key]
        except Exception as e:
            logger.error(f"Cache get error: {e}")

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL in seconds."""
        try:
            if self._redis_client:
                return bool(self._redis_client.setex(key, ttl or 3600, json.dumps(value)))
            else:
                # Memory cache
                expiry = time.time() + (ttl or 3600) if ttl else None
                self._memory_cache[key] = (value, expiry)
                return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            if self._redis_client:
                return bool(self._redis_client.delete(key))
            else:
                if key in self._memory_cache:
                    del self._memory_cache[key]
                    return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

        return False

    def clear(self) -> bool:
        """Clear all cache entries."""
        try:
            if self._redis_client:
                return bool(self._redis_client.flushdb())
            else:
                self._memory_cache.clear()
                return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False

    def get_or_set(self, key: str, func, ttl: Optional[int] = None):
        """Get value from cache or compute and cache it."""
        value = self.get(key)
        if value is not None:
            return value

        value = func()
        self.set(key, value, ttl)
        return value

# Global cache instance
_cache_instance = None

def get_cache() -> Cache:
    """Get the global cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = Cache()
    return _cache_instance

# Cache key generators
def user_profile_cache_key(user_id: int) -> str:
    """Generate cache key for user profile."""
    return f"user:profile:{user_id}"

def watchlist_cache_key(user_id: int, status_filter: Optional[str] = None) -> str:
    """Generate cache key for user's watchlist."""
    if status_filter:
        return f"user:watchlist:{user_id}:status:{status_filter}"
    return f"user:watchlist:{user_id}"

def watchlist_stats_cache_key(user_id: int) -> str:
    """Generate cache key for watchlist statistics."""
    return f"user:watchlist:stats:{user_id}"
