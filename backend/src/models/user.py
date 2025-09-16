"""
User and Watchlist SQLModel models.
Defines database schema with proper relationships and constraints.
"""

from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .watchlist import WatchlistItem


class UserBase(SQLModel):
    """Base user model with common fields."""

    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: EmailStr = Field(index=True, unique=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """
    User database model.

    Links to SuperTokens user ID and stores additional user data.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    supertokens_user_id: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    watchlist_items: list["WatchlistItem"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """Schema for creating a new user."""

    supertokens_user_id: str


class UserUpdate(SQLModel):
    """Schema for updating user information."""

    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = None


class UserRead(UserBase):
    """Schema for reading user information (public)."""

    id: int
    created_at: datetime
    updated_at: datetime
