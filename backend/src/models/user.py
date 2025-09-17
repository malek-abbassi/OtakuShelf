"""
User and Watchlist SQLModel models.
Defines database schema with proper relationships and constraints.
"""

from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING, List

from pydantic import EmailStr, field_validator, computed_field
from sqlmodel import SQLModel, Field, Relationship, Column, String, Boolean, DateTime, Integer, Index
from sqlalchemy import func

if TYPE_CHECKING:
    from .watchlist import WatchlistItem


class UserBase(SQLModel):
    """Base user model with common fields."""

    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: EmailStr = Field(index=True, unique=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")
        if v.startswith("_") or v.startswith("-") or v.endswith("_") or v.endswith("-"):
            raise ValueError("Username cannot start or end with underscores or hyphens")
        return v.lower()

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean full name."""
        if v is None:
            return v
        cleaned = " ".join(v.split())  # Remove extra whitespace
        if len(cleaned) < 2:
            raise ValueError("Full name must be at least 2 characters long")
        return cleaned.title() if cleaned else None


class User(UserBase, table=True):
    """
    User database model.

    Links to SuperTokens user ID and stores additional user data.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    supertokens_user_id: str = Field(
        index=True,
        unique=True,
        min_length=1,
        max_length=128,
        description="SuperTokens user ID"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )

    # Relationships
    watchlist_items: List["WatchlistItem"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # Indexes
    __table_args__ = (
        Index("ix_user_active_created", "is_active", "created_at"),
        Index("ix_user_email_active", "email", "is_active"),
    )

    @computed_field
    @property
    def watchlist_count(self) -> int:
        """Get the number of items in the user's watchlist."""
        return len(self.watchlist_items) if self.watchlist_items else 0

    @computed_field
    @property
    def account_age_days(self) -> int:
        """Get the age of the account in days."""
        now = datetime.now(UTC)
        # Ensure created_at is offset-aware
        created_at = self.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)
        return (now - created_at).days

    def is_account_new(self, days: int = 7) -> bool:
        """Check if the account is newer than the specified number of days."""
        return self.account_age_days <= days

    def can_modify_profile(self) -> bool:
        """Check if the user can modify their profile."""
        return self.is_active

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.now(UTC)

    def reactivate(self) -> None:
        """Reactivate the user account."""
        self.is_active = True
        self.updated_at = datetime.now(UTC)


class UserCreate(UserBase):
    """Schema for creating a new user."""

    supertokens_user_id: str


class UserUpdate(SQLModel):
    """Schema for updating user information."""

    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        """Validate username format if provided."""
        if v is None:
            return v
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")
        if v.startswith("_") or v.startswith("-") or v.endswith("_") or v.endswith("-"):
            raise ValueError("Username cannot start or end with underscores or hyphens")
        return v.lower()

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean full name if provided."""
        if v is None:
            return v
        cleaned = " ".join(v.split())  # Remove extra whitespace
        if len(cleaned) < 2:
            raise ValueError("Full name must be at least 2 characters long")
        return cleaned.title() if cleaned else None


class UserRead(UserBase):
    """Schema for reading user information (public)."""

    id: int
    created_at: datetime
    updated_at: datetime
    watchlist_count: int
    account_age_days: int
