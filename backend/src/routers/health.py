"""
Health check and monitoring endpoints.
Provides system health status, metrics, and diagnostics.
"""

import time
import psutil
import sys
from typing import Dict, Any
from datetime import datetime, UTC

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..db.core import get_session, engine
from ..cache import get_cache
from ..rate_limit import get_rate_limiter
from ..config import get_settings

router = APIRouter(prefix="/health", tags=["health"])
settings = get_settings()

# Track application startup time
START_TIME = time.time()

@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "service": settings.app_name,
        "environment": settings.environment
    }

@router.get("/detailed")
async def detailed_health_check(
    db: Session = Depends(get_session)
) -> Dict[str, Any]:
    """Detailed health check with system metrics."""

    # Database health check
    db_healthy = True
    db_error = None
    try:
        # Simple query to test database connection
        db.exec("SELECT 1")
    except Exception as e:
        db_healthy = False
        db_error = str(e)

    # Cache health check
    cache_healthy = True
    cache_error = None
    try:
        cache = get_cache()
        # Simple cache test
        test_key = "health_check_test"
        cache.set(test_key, "ok", ttl=10)
        result = cache.get(test_key)
        cache.delete(test_key)
        if result != "ok":
            cache_healthy = False
            cache_error = "Cache set/get failed"
    except Exception as e:
        cache_healthy = False
        cache_error = str(e)

    # Rate limiter health check
    rate_limiter_healthy = True
    rate_limiter_error = None
    try:
        limiter = get_rate_limiter()
        # Simple rate limiter test
        test_key = "health_check_rate_limit"
        is_allowed = limiter.is_allowed(test_key, 10, 60)
        if not isinstance(is_allowed, bool):
            rate_limiter_healthy = False
            rate_limiter_error = "Rate limiter returned invalid response"
    except Exception as e:
        rate_limiter_healthy = False
        rate_limiter_error = str(e)

    # System metrics
    system_metrics = {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent,
    }

    # Application metrics
    app_metrics = {
        "uptime_seconds": time.time() - START_TIME,
        "python_version": f"{sys.version}",
    }

    # Overall health status
    overall_healthy = all([
        db_healthy,
        cache_healthy,
        rate_limiter_healthy
    ])

    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "service": settings.app_name,
        "environment": settings.environment,
        "checks": {
            "database": {
                "healthy": db_healthy,
                "error": db_error
            },
            "cache": {
                "healthy": cache_healthy,
                "error": cache_error
            },
            "rate_limiter": {
                "healthy": rate_limiter_healthy,
                "error": rate_limiter_error
            }
        },
        "metrics": {
            "system": system_metrics,
            "application": app_metrics
        }
    }

@router.get("/database")
async def database_health_check(db: Session = Depends(get_session)) -> Dict[str, Any]:
    """Database-specific health check."""
    try:
        # Test database connection and basic query
        result = db.exec("SELECT 1 as test").first()
        if result and result.test == 1:
            return {
                "status": "healthy",
                "database_type": "sqlite" if "sqlite" in str(engine.url) else "postgresql",
                "connection_pool": {
                    "size": getattr(engine.pool, 'size', 'N/A'),
                    "checked_out": getattr(engine.pool, 'checkedout', 'N/A'),
                }
            }
        else:
            return {"status": "unhealthy", "error": "Database query failed"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@router.get("/metrics")
async def metrics() -> Dict[str, Any]:
    """Application metrics endpoint."""
    return {
        "uptime_seconds": time.time() - START_TIME,
        "start_time": datetime.fromtimestamp(START_TIME, UTC).isoformat(),
        "environment": settings.environment,
        "system": {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "memory_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
            "disk_used_gb": round(psutil.disk_usage('/').used / (1024**3), 2),
            "disk_percent": psutil.disk_usage('/').percent,
        }
    }
