"""
Watchlist SQLModel models.
Defines anime watchlist schema with relationships to users.
"""

from datetime import datetime, UTC
from enum import Enum
from typing import Optional, TYPE_CHECKING

from pydantic import field_validator, computed_field
from sqlmodel import SQLModel, Field, Relationship, Index

if TYPE_CHECKING:
    from .user import User


class WatchStatus(str, Enum):
    """Enum for watchlist item status."""
    PLAN_TO_WATCH = "plan_to_watch"
    WATCHING = "watching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"

    @property
    def is_active(self) -> bool:
        """Check if this status represents active watching."""
        return self in (WatchStatus.WATCHING, WatchStatus.PLAN_TO_WATCH)

    @property
    def is_finished(self) -> bool:
        """Check if this status represents a finished state."""
        return self in (WatchStatus.COMPLETED, WatchStatus.DROPPED)


class WatchlistItemBase(SQLModel):
    """Base watchlist item model with anime information."""

    anime_id: int = Field(
        description="AniList anime ID",
        gt=0,
        index=True
    )
    anime_title: str = Field(
        min_length=1,
        max_length=200,
        description="Anime title"
    )
    anime_picture_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Anime poster/cover image URL"
    )
    anime_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=10.0,
        description="Anime score/rating"
    )
    status: WatchStatus = Field(
        default=WatchStatus.PLAN_TO_WATCH,
        description="Watch status"
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="User notes about the anime"
    )

    @field_validator('anime_picture_url')
    @classmethod
    def validate_anime_picture_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate anime picture URL format."""
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Anime picture URL must be a valid HTTP/HTTPS URL')
        return v

    @field_validator('anime_title')
    @classmethod
    def validate_anime_title(cls, v: str) -> str:
        """Validate and clean anime title."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Anime title cannot be empty")
        return cleaned

    @field_validator("anime_score")
    @classmethod
    def validate_anime_score(cls, v: Optional[float]) -> Optional[float]:
        """Validate anime score."""
        if v is None:
            return v
        if not (0.0 <= v <= 10.0):
            raise ValueError("Anime score must be between 0.0 and 10.0")
        return round(v, 1)  # Round to 1 decimal place

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean notes."""
        if v is None:
            return v
        cleaned = v.strip()
        if len(cleaned) > 1000:
            raise ValueError("Notes cannot exceed 1000 characters")
        return cleaned if cleaned else None


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

    # Indexes
    __table_args__ = (
        Index("ix_watchlist_user_status", "user_id", "status"),
        Index("ix_watchlist_user_anime", "user_id", "anime_id", unique=True),
        Index("ix_watchlist_status_created", "status", "created_at"),
        Index("ix_watchlist_score", "anime_score"),
        Index("ix_watchlist_user_created", "user_id", "created_at"),
        Index("ix_watchlist_user_updated", "user_id", "updated_at"),
        Index("ix_watchlist_anime_status", "anime_id", "status"),
    )

    @computed_field
    @property
    def days_since_added(self) -> int:
        """Get the number of days since this item was added."""
        now = datetime.now(UTC)
        # Ensure created_at is offset-aware
        created_at = self.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)
        return (now - created_at).days

    @computed_field
    @property
    def days_since_updated(self) -> int:
        """Get the number of days since this item was last updated."""
        now = datetime.now(UTC)
        # Ensure updated_at is offset-aware
        updated_at = self.updated_at
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=UTC)
        return (now - updated_at).days

    def is_recently_added(self, days: int = 7) -> bool:
        """Check if the item was added within the specified number of days."""
        return self.days_since_added <= days

    def is_recently_updated(self, days: int = 7) -> bool:
        """Check if the item was updated within the specified number of days."""
        return self.days_since_updated <= days

    def mark_as_updated(self) -> None:
        """Mark the item as updated."""
        self.updated_at = datetime.now(UTC)

    def change_status(self, new_status: WatchStatus) -> None:
        """Change the watch status and update timestamp."""
        self.status = new_status
        self.mark_as_updated()

    def update_score(self, score: Optional[float]) -> None:
        """Update the anime score."""
        self.anime_score = score
        self.mark_as_updated()

    def update_notes(self, notes: Optional[str]) -> None:
        """Update the notes."""
        self.notes = notes
        self.mark_as_updated()


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

    @field_validator("anime_title")
    @classmethod
    def validate_anime_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate anime title if provided."""
        if v is None:
            return v
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Anime title cannot be empty")
        if len(cleaned) > 200:
            raise ValueError("Anime title cannot exceed 200 characters")
        return cleaned

    @field_validator("anime_picture_url")
    @classmethod
    def validate_anime_picture_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate anime picture URL if provided."""
        if v is None:
            return v
        if not v.startswith(("http://", "https://")):
            raise ValueError("Anime picture URL must be a valid HTTP/HTTPS URL")
        return v

    @field_validator("anime_score")
    @classmethod
    def validate_anime_score(cls, v: Optional[float]) -> Optional[float]:
        """Validate anime score if provided."""
        if v is None:
            return v
        if not (0.0 <= v <= 10.0):
            raise ValueError("Anime score must be between 0.0 and 10.0")
        return round(v, 1)  # Round to 1 decimal place

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean notes if provided."""
        if v is None:
            return v
        cleaned = v.strip()
        if len(cleaned) > 1000:
            raise ValueError("Notes cannot exceed 1000 characters")
        return cleaned if cleaned else None


class WatchlistItemRead(WatchlistItemBase):
    """Schema for reading watchlist item information."""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    days_since_added: int
    days_since_updated: int


class WatchlistItemReadWithUser(WatchlistItemRead):
    """Schema for reading watchlist item with user information."""

    user: Optional["UserRead"] = None


# Import here to avoid circular imports
from .user import UserRead  # noqa: E402

# Update forward references
WatchlistItemReadWithUser.model_rebuild()
