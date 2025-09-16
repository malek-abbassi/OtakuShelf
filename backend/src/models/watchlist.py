"""
Watchlist SQLModel models.
Defines anime watchlist schema with relationships to users.
"""

from datetime import datetime, UTC
from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


class WatchStatus(str, Enum):
    """Enum for watchlist item status."""
    PLAN_TO_WATCH = "plan_to_watch"
    WATCHING = "watching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"


class WatchlistItemBase(SQLModel):
    """Base watchlist item model with anime information."""

    anime_id: int = Field(description="AniList anime ID")
    anime_title: str = Field(max_length=200, description="Anime title")
    anime_picture_url: Optional[str] = Field(
        default=None, description="Anime poster/cover image URL"
    )
    anime_score: Optional[float] = Field(
        default=None, ge=0.0, le=10.0, description="Anime score/rating"
    )
    status: WatchStatus = Field(default=WatchStatus.PLAN_TO_WATCH, description="Watch status")
    notes: Optional[str] = Field(
        default=None, max_length=1000, description="User notes about the anime"
    )


class WatchlistItem(WatchlistItemBase, table=True):
    """
    Watchlist item database model.

    Stores anime information that a user wants to watch.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    user: "User" = Relationship(back_populates="watchlist_items")


class WatchlistItemCreate(WatchlistItemBase):
    """Schema for creating a new watchlist item."""

    pass


class WatchlistItemUpdate(SQLModel):
    """Schema for updating a watchlist item."""

    anime_title: Optional[str] = Field(default=None, max_length=200)
    anime_picture_url: Optional[str] = None
    anime_score: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    status: Optional[WatchStatus] = None
    notes: Optional[str] = Field(default=None, max_length=1000)


class WatchlistItemRead(WatchlistItemBase):
    """Schema for reading watchlist item information."""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class WatchlistItemReadWithUser(WatchlistItemRead):
    """Schema for reading watchlist item with user information."""

    user: Optional["UserRead"] = None


# Import here to avoid circular imports
from .user import UserRead  # noqa: E402

# Update forward references
WatchlistItemReadWithUser.model_rebuild()
