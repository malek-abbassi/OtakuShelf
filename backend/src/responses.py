"""
Custom response classes for consistent API responses.
"""

from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""

    success: bool = Field(default=True, description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    data: Optional[T] = Field(default=None, description="Response data")
    error_code: Optional[str] = Field(default=None, description="Error code if applicable")

    @classmethod
    def success_response(
        cls,
        message: str = "Success",
        data: Optional[T] = None
    ) -> "APIResponse[T]":
        """Create a successful response."""
        return cls(message=message, data=data)

    @classmethod
    def error_response(
        cls,
        message: str,
        error_code: Optional[str] = None,
        data: Optional[T] = None
    ) -> "APIResponse[T]":
        """Create an error response."""
        return cls(
            success=False,
            message=message,
            data=data,
            error_code=error_code
        )


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""

    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(default=1, description="Current page number")
    page_size: int = Field(default=20, description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int = 1,
        page_size: int = 20
    ) -> "PaginatedResponse[T]":
        """Create a paginated response."""
        total_pages = (total + page_size - 1) // page_size  # Ceiling division
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Deployment environment")
    timestamp: float = Field(..., description="Response timestamp")
    database: bool = Field(default=True, description="Database connectivity status")
    uptime: Optional[float] = Field(default=None, description="Service uptime in seconds")
