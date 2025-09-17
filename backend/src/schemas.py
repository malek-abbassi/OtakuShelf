"""
API schemas for request/response data validation.
Separate from database models for clean API contracts.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Any, Dict
from re import match

from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, computed_field


class WatchStatus(str, Enum):
    """Enum for watchlist item status."""
    PLAN_TO_WATCH = "plan_to_watch"
    WATCHING = "watching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    detail: str
    error_code: Optional[str] = None


class SuccessResponse(BaseModel):
    """Standard success response schema."""

    message: str
    data: Optional[dict] = None


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""

    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(
        default=20, ge=1, le=100, description="Number of items to return"
    )


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""

    items: List[Any] = Field(..., description="List of items")
    total: int = Field(..., ge=0, description="Total number of items")
    skip: int = Field(..., ge=0, description="Number of items skipped")
    limit: int = Field(..., ge=1, description="Number of items per page")

    @computed_field
    @property
    def has_next(self) -> bool:
        """Check if there are more items available."""
        return self.skip + self.limit < self.total

    @computed_field
    @property
    def has_prev(self) -> bool:
        """Check if there are previous items available."""
        return self.skip > 0


# User-specific schemas
class UserLoginRequest(BaseModel):
    """User login request schema."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', v):
            raise ValueError('Password must contain at least one lowercase letter, one uppercase letter, and one digit')
        return v


class UserSignupRequest(BaseModel):
    """User signup request schema."""

    email: EmailStr = Field(..., description="User email address", examples=["user@example.com"])
    password: str = Field(..., min_length=8, description="User password", examples=["SecurePass123"])
    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username", examples=["animefan123"]
    )
    full_name: Optional[str] = Field(
        default=None, max_length=100, description="User's full name", examples=["John Doe"]
    )

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        if not match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', v):
            raise ValueError('Password must contain at least one lowercase letter, one uppercase letter, and one digit')
        return v

    @model_validator(mode='after')
    def validate_full_name_not_empty(self):
        """Ensure full name is not empty if provided."""
        if self.full_name is not None and self.full_name.strip() == "":
            raise ValueError("Full name cannot be empty if provided")
        return self


class UserProfileResponse(BaseModel):
    """User profile response schema."""

    id: int = Field(..., gt=0, description="User ID")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(default=None, max_length=100, description="User's full name")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")
    watchlist_count: int = Field(..., ge=0, description="Number of items in watchlist")

    @computed_field
    @property
    def account_age_days(self) -> int:
        """Calculate account age in days."""
        return (datetime.now() - self.created_at.replace(tzinfo=None)).days

    @computed_field
    @property
    def display_name(self) -> str:
        """Get display name (full name if available, otherwise username)."""
        return self.full_name if self.full_name else self.username


# Watchlist-specific schemas
class AnimeSearchResult(BaseModel):
    """Anime search result from external API."""

    id: int = Field(..., gt=0, description="AniList anime ID")
    title: str = Field(..., min_length=1, max_length=200, description="Anime title")
    cover_image: Optional[str] = Field(default=None, description="Cover image URL")
    score: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Average score")
    genres: List[str] = Field(default_factory=list, description="Anime genres")
    status: Optional[str] = Field(default=None, description="Anime status")

    @field_validator('cover_image')
    @classmethod
    def validate_cover_image_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate cover image URL format."""
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Cover image must be a valid HTTP/HTTPS URL')
        return v


class WatchlistAddRequest(BaseModel):
    """Request to add anime to watchlist."""

    animeId: int = Field(..., alias="anime_id", gt=0, description="AniList anime ID", examples=[12345])
    animeTitle: str = Field(..., alias="anime_title", min_length=1, max_length=200, description="Anime title", examples=["Attack on Titan"])
    animePictureUrl: Optional[str] = Field(
        default=None, alias="anime_picture_url", description="Anime cover image URL", examples=["https://example.com/image.jpg"]
    )
    animeScore: Optional[float] = Field(
        default=None, alias="anime_score", ge=0.0, le=10.0, description="Anime score", examples=[8.5]
    )
    status: WatchStatus = Field(default=WatchStatus.PLAN_TO_WATCH, description="Watch status")
    notes: Optional[str] = Field(
        default=None, max_length=1000, description="User notes", examples=["Looking forward to watching this!"]
    )

    model_config = {"populate_by_name": True}

    @field_validator('animePictureUrl')
    @classmethod
    def validate_anime_picture_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate anime picture URL format."""
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Anime picture URL must be a valid HTTP/HTTPS URL')
        return v

    @model_validator(mode="after")
    def validate_anime_title_not_empty(self):
        """Ensure anime title is not empty after stripping whitespace."""
        if not self.animeTitle or self.animeTitle.strip() == "":
            raise ValueError("Anime title cannot be empty")
        return self


class WatchlistUpdateRequest(BaseModel):
    """Request to update watchlist item."""

    status: Optional[WatchStatus] = Field(default=None, description="Watch status")
    notes: Optional[str] = Field(
        default=None, max_length=1000, description="User notes"
    )
    animeScore: Optional[float] = Field(
        default=None, alias="anime_score", ge=0.0, le=10.0, description="User rating"
    )

    model_config = {"populate_by_name": True}


class WatchlistItemResponse(BaseModel):
    """Watchlist item response schema."""

    id: int = Field(..., gt=0, description="Watchlist item ID")
    animeId: int = Field(..., alias="anime_id", gt=0, description="AniList anime ID")
    animeTitle: str = Field(..., alias="anime_title", min_length=1, max_length=200, description="Anime title")
    animePictureUrl: Optional[str] = Field(..., alias="anime_picture_url", description="Anime cover image URL")
    animeScore: Optional[float] = Field(..., alias="anime_score", ge=0.0, le=10.0, description="Anime score")
    status: WatchStatus = Field(..., description="Watch status")
    notes: Optional[str] = Field(..., max_length=1000, description="User notes")
    createdAt: datetime = Field(..., alias="created_at", description="Item creation timestamp")
    updatedAt: datetime = Field(..., alias="updated_at", description="Item last update timestamp")

    model_config = {"populate_by_name": True}

    @computed_field
    @property
    def days_since_added(self) -> int:
        """Calculate days since the item was added to watchlist."""
        return (datetime.now() - self.createdAt.replace(tzinfo=None)).days

    @computed_field
    @property
    def is_recently_updated(self) -> bool:
        """Check if the item was updated recently (within last 24 hours)."""
        return (datetime.now() - self.updatedAt.replace(tzinfo=None)).total_seconds() < 86400


class WatchlistResponse(BaseModel):
    """User's watchlist response schema."""

    items: List[WatchlistItemResponse] = Field(..., description="List of watchlist items")
    totalCount: int = Field(..., alias="total_count", ge=0, description="Total number of items")
    statusCounts: Dict[str, int] = Field(..., alias="status_counts", description="Count of items by status")

    model_config = {"populate_by_name": True}

    @computed_field
    @property
    def completion_rate(self) -> float:
        """Calculate the completion rate as a percentage."""
        if self.totalCount == 0:
            return 0.0
        completed = self.statusCounts.get(WatchStatus.COMPLETED, 0)
        return round((completed / self.totalCount) * 100, 1)
