"""
API schemas for request/response data validation.
Separate from database models for clean API contracts.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


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

    items: list
    total: int
    skip: int
    limit: int
    has_next: bool


# User-specific schemas
class UserLoginRequest(BaseModel):
    """User login request schema."""

    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")


class UserSignupRequest(BaseModel):
    """User signup request schema."""

    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username"
    )
    full_name: Optional[str] = Field(
        default=None, max_length=100, description="User's full name"
    )


class UserProfileResponse(BaseModel):
    """User profile response schema."""

    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    watchlist_count: int


# Watchlist-specific schemas
class AnimeSearchResult(BaseModel):
    """Anime search result from external API."""

    id: int = Field(..., description="AniList anime ID")
    title: str = Field(..., description="Anime title")
    cover_image: Optional[str] = Field(default=None, description="Cover image URL")
    score: Optional[float] = Field(default=None, description="Average score")
    genres: list[str] = Field(default_factory=list, description="Anime genres")
    status: Optional[str] = Field(default=None, description="Anime status")


class WatchlistAddRequest(BaseModel):
    """Request to add anime to watchlist."""

    animeId: int = Field(..., alias="anime_id", description="AniList anime ID")
    animeTitle: str = Field(..., alias="anime_title", max_length=200, description="Anime title")
    animePictureUrl: Optional[str] = Field(
        default=None, alias="anime_picture_url", description="Anime cover image URL"
    )
    animeScore: Optional[float] = Field(
        default=None, alias="anime_score", ge=0.0, le=10.0, description="Anime score"
    )
    status: str = Field(default="plan_to_watch", description="Watch status")
    notes: Optional[str] = Field(
        default=None, max_length=1000, description="User notes"
    )

    model_config = {"populate_by_name": True}


class WatchlistUpdateRequest(BaseModel):
    """Request to update watchlist item."""

    status: Optional[str] = Field(default=None, description="Watch status")
    notes: Optional[str] = Field(
        default=None, max_length=1000, description="User notes"
    )
    animeScore: Optional[float] = Field(
        default=None, alias="anime_score", ge=0.0, le=10.0, description="User rating"
    )

    model_config = {"populate_by_name": True}


class WatchlistItemResponse(BaseModel):
    """Watchlist item response schema."""

    id: int
    animeId: int = Field(alias="anime_id")
    animeTitle: str = Field(alias="anime_title") 
    animePictureUrl: Optional[str] = Field(alias="anime_picture_url")
    animeScore: Optional[float] = Field(alias="anime_score")
    status: str
    notes: Optional[str]
    createdAt: datetime = Field(alias="created_at")
    updatedAt: datetime = Field(alias="updated_at")

    model_config = {"populate_by_name": True}


class WatchlistResponse(BaseModel):
    """User's watchlist response schema."""

    items: list[WatchlistItemResponse]
    totalCount: int = Field(alias="total_count")
    statusCounts: dict[str, int] = Field(alias="status_counts")

    model_config = {"populate_by_name": True}
