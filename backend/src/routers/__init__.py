"""
API routers package.
Exports all FastAPI routers for the application.
"""

from .users import router as users_router
from .watchlist import router as watchlist_router
from .health import router as health_router

__all__ = [
    "users_router",
    "watchlist_router",
    "health_router",
]
