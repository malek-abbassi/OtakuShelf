"""
Custom exception classes and error handling for the API.
Provides consistent error responses and structured error information.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class OtakuShelfException(Exception):
    """Base exception class for OtakuShelf API errors with structured error information."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.headers = headers
        super().__init__(message)


class AuthenticationError(OtakuShelfException):
    """Exception raised for authentication-related errors."""

    def __init__(
        self,
        message: str = "Authentication required",
        error_code: str = "AUTHENTICATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=error_code,
            details=details,
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationError(OtakuShelfException):
    """Exception raised for authorization-related errors."""

    def __init__(
        self,
        message: str = "Insufficient permissions",
        error_code: str = "AUTHORIZATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code,
            details=details
        )


class NotFoundError(OtakuShelfException):
    """Exception raised when a resource is not found."""

    def __init__(
        self,
        resource: str,
        resource_id: Optional[Any] = None,
        error_code: str = "NOT_FOUND",
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"{resource} not found"
        if resource_id is not None:
            message += f" with ID: {resource_id}"

        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code,
            details={"resource": resource, "resource_id": resource_id, **(details or {})}
        )


class ValidationError(OtakuShelfException):
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        error_code: str = "VALIDATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=error_code,
            details={"field": field, **(details or {})}
        )


class ConflictError(OtakuShelfException):
    """Exception raised for conflicts (e.g., duplicate resources)."""

    def __init__(
        self,
        message: str,
        error_code: str = "CONFLICT",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code,
            details=details or {}
        )


class RateLimitError(OtakuShelfException):
    """Exception raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        error_code: str = "RATE_LIMIT_EXCEEDED",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code=error_code,
            details={"retry_after": retry_after, **(details or {})},
            headers={"Retry-After": str(retry_after)} if retry_after else None
        )


class ServiceUnavailableError(OtakuShelfException):
    """Exception raised when a service is unavailable."""

    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        error_code: str = "SERVICE_UNAVAILABLE",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code=error_code,
            details=details or {}
        )


class DatabaseError(OtakuShelfException):
    """Exception raised for database-related errors."""

    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        error_code: str = "DATABASE_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
            details={"operation": operation, **(details or {})}
        )


# Business logic specific exceptions
class UserNotFoundError(NotFoundError):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: Optional[int] = None, username: Optional[str] = None):
        if user_id:
            super().__init__("User", user_id)
        elif username:
            super().__init__("User", f"username:{username}", {"username": username})
        else:
            super().__init__("User")


class WatchlistItemNotFoundError(NotFoundError):
    """Exception raised when a watchlist item is not found."""

    def __init__(self, item_id: Optional[int] = None, anime_id: Optional[int] = None, user_id: Optional[int] = None):
        details = {}
        if user_id:
            details["user_id"] = user_id

        if item_id:
            super().__init__("Watchlist item", item_id, details)
        elif anime_id:
            super().__init__("Watchlist item", f"anime_id:{anime_id}", {**details, "anime_id": anime_id})
        else:
            super().__init__("Watchlist item", details=details)


class DuplicateWatchlistItemError(ConflictError):
    """Exception raised when trying to add a duplicate anime to watchlist."""

    def __init__(self, anime_id: int):
        super().__init__(
            f"Anime with ID {anime_id} is already in your watchlist",
            details={"anime_id": anime_id}
        )


class InactiveUserError(AuthorizationError):
    """Exception raised when trying to perform actions on an inactive user account."""

    def __init__(self, user_id: int):
        super().__init__(
            "User account is inactive",
            details={"user_id": user_id}
        )


class InvalidWatchStatusError(ValidationError):
    """Exception raised when an invalid watch status is provided."""

    def __init__(self, status: str, valid_statuses: list[str]):
        super().__init__(
            f"Invalid watch status: {status}",
            field="status",
            details={"provided": status, "valid_options": valid_statuses}
        )


class RateLimitExceededError(OtakuShelfException):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, limit: int, window: int, remaining: int, reset_time: int):
        super().__init__(
            f"Rate limit exceeded. {remaining} requests remaining.",
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            details={
                "limit": limit,
                "window": window,
                "remaining": remaining,
                "reset_time": reset_time
            },
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(reset_time),
                "Retry-After": str(reset_time)
            }
        )


def create_error_response(exception: OtakuShelfException) -> Dict[str, Any]:
    """Create a consistent error response dictionary from an exception."""
    return {
        "error": {
            "code": exception.error_code,
            "message": exception.message,
            "details": exception.details
        }
    }


def create_http_exception(exception: OtakuShelfException) -> HTTPException:
    """Convert an OtakuShelfException to a FastAPI HTTPException with consistent format."""
    return HTTPException(
        status_code=exception.status_code,
        detail=create_error_response(exception),
        headers=exception.headers
    )
