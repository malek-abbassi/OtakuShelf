"""
Database models package.
Exports all SQLModel models for the application.
"""

from .user import User, UserBase, UserCreate, UserUpdate, UserRead
from .watchlist import (
    WatchlistItem,
    WatchlistItemBase,
    WatchlistItemCreate,
    WatchlistItemUpdate,
    WatchlistItemRead,
    WatchlistItemReadWithUser,
)

__all__ = [
    # User models
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserRead",
    # Watchlist models
    "WatchlistItem",
    "WatchlistItemBase",
    "WatchlistItemCreate",
    "WatchlistItemUpdate",
    "WatchlistItemRead",
    "WatchlistItemReadWithUser",
]
