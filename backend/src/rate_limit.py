"""
Rate limiting functionality to prevent abuse.
Provides configurable rate limits with Redis backend.
"""

import logging
import time
from functools import wraps

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from .config import get_settings
from .exceptions import RateLimitExceededError

logger = logging.getLogger(__name__)
settings = get_settings()

class RateLimiter:
    """Rate limiter using Redis or in-memory storage."""

    def __init__(self):
        self._memory_limits = {}
        self._redis_client = None

        if REDIS_AVAILABLE and settings.redis_url:
            try:
                self._redis_client = redis.from_url(settings.redis_url)
                self._redis_client.ping()
                logger.info("Redis rate limiter initialized")
            except Exception as e:
                logger.warning(f"Redis connection failed for rate limiting: {e}")
                self._redis_client = None
        else:
            logger.info("Using in-memory rate limiter")

    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """
        Check if request is allowed under rate limit.

        Args:
            key: Unique identifier for the rate limit (e.g., "user:123:login")
            limit: Maximum number of requests allowed
            window: Time window in seconds

        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        try:
            current_time = int(time.time())

            if self._redis_client:
                # Use Redis sorted set for sliding window
                pipeline = self._redis_client.pipeline()
                # Remove old entries outside the window
                pipeline.zremrangebyscore(key, 0, current_time - window)
                # Add current request
                pipeline.zadd(key, {str(current_time): current_time})
                # Count requests in window
                pipeline.zcard(key)
                # Set expiry on the key
                pipeline.expire(key, window)

                results = pipeline.execute()
                request_count = results[2]

                return request_count <= limit
            else:
                # In-memory rate limiting (less accurate)
                if key not in self._memory_limits:
                    self._memory_limits[key] = []

                # Clean old entries
                cutoff = current_time - window
                self._memory_limits[key] = [
                    ts for ts in self._memory_limits[key] if ts > cutoff
                ]

                # Check if under limit
                if len(self._memory_limits[key]) < limit:
                    self._memory_limits[key].append(current_time)
                    return True

                return False

        except Exception as e:
            logger.error(f"Rate limit check error: {e}")
            # Allow request on error to avoid blocking legitimate traffic
            return True

    def get_remaining_requests(self, key: str, limit: int, window: int) -> int:
        """Get remaining requests allowed in current window."""
        try:
            current_time = int(time.time())

            if self._redis_client:
                # Clean old entries and count current ones
                pipeline = self._redis_client.pipeline()
                pipeline.zremrangebyscore(key, 0, current_time - window)
                pipeline.zcard(key)
                results = pipeline.execute()
                current_count = results[1]
            else:
                if key in self._memory_limits:
                    cutoff = current_time - window
                    current_count = len([
                        ts for ts in self._memory_limits[key] if ts > cutoff
                    ])
                else:
                    current_count = 0

            return max(0, limit - current_count)

        except Exception as e:
            logger.error(f"Error getting remaining requests: {e}")
            return limit

    def reset_limit(self, key: str) -> bool:
        """Reset rate limit for a key."""
        try:
            if self._redis_client:
                return bool(self._redis_client.delete(key))
            else:
                if key in self._memory_limits:
                    del self._memory_limits[key]
                    return True
                return False
        except Exception as e:
            logger.error(f"Error resetting rate limit: {e}")
            return False

# Global rate limiter instance
_rate_limiter_instance = None

def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    global _rate_limiter_instance
    if _rate_limiter_instance is None:
        _rate_limiter_instance = RateLimiter()
    return _rate_limiter_instance

# Rate limit configurations
RATE_LIMITS = {
    "auth_login": {"limit": 5, "window": 300},  # 5 login attempts per 5 minutes
    "auth_register": {"limit": 3, "window": 3600},  # 3 registrations per hour
    "api_general": {"limit": 100, "window": 60},  # 100 requests per minute
    "api_watchlist": {"limit": 50, "window": 60},  # 50 watchlist operations per minute
}

def rate_limit(limit_name: str):
    """
    Decorator to apply rate limiting to API endpoints.

    Usage:
        @rate_limit("api_general")
        async def my_endpoint():
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user identifier from request
            # This is a simplified version - in practice you'd get user ID from auth context
            user_id = "anonymous"

            # Try to get request from args (FastAPI dependency injection)
            for arg in args:
                if hasattr(arg, 'client'):  # FastAPI Request object
                    request = arg
                    break

            if request:
                try:
                    from .dependencies import get_current_user_optional
                    user = await get_current_user_optional(request)
                    if user:
                        user_id = str(user.id)
                except Exception:
                    pass  # Keep anonymous if auth fails

            limiter = get_rate_limiter()
            key = f"{limit_name}:{user_id}"

            config = RATE_LIMITS.get(limit_name, RATE_LIMITS["api_general"])

            if not limiter.is_allowed(key, config["limit"], config["window"]):
                remaining = limiter.get_remaining_requests(key, config["limit"], config["window"])
                reset_time = config["window"]

                raise RateLimitExceededError(
                    limit=config["limit"],
                    window=config["window"],
                    remaining=remaining,
                    reset_time=reset_time
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator
