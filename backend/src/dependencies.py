"""
Application dependencies and middleware.
Provides dependency injection and error handling.
"""

import logging
import time
from typing import Annotated, Generator

from fastapi import Depends, Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session

from .auth import AuthService
from .db.core import get_session, engine
from .config import get_settings
from .exceptions import OtakuShelfException
from .responses import HealthResponse
from .services.user_service import UserService
from .services.watchlist_service import WatchlistService

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging."""

    async def dispatch(self, request: Request, call_next):
        # Log request with timing
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url}")

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response with timing
        logger.info(
            f"Response: {response.status_code} - "
            f"{request.method} {request.url} - "
            f"Duration: {process_time:.4f}s"
        )

        # Add processing time to response headers
        response.headers["X-Process-Time"] = str(process_time)

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling with consistent error responses."""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except OtakuShelfException as e:
            # Handle custom OtakuShelf exceptions with structured error response
            from .exceptions import create_error_response
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    **create_error_response(e)
                },
                headers=e.headers
            )
        except HTTPException as e:
            # Handle FastAPI HTTP exceptions
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "error": {
                        "code": getattr(e, "error_code", "HTTP_EXCEPTION"),
                        "message": e.detail,
                        "details": {}
                    }
                },
                headers=getattr(e, "headers", None),
            )
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)

            # Return generic error response
            error_detail = "Internal server error" if settings.environment == "production" else str(e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": error_detail,
                        "details": {}
                    }
                },
            )


# Database dependency with proper error handling
def get_db_session() -> Generator[Session, None, None]:
    """
    Database session dependency with error handling.

    Yields:
        Session: SQLModel database session
    """
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error",
        )


# Common dependencies
DatabaseDep = Annotated[Session, Depends(get_session)]


def get_auth_service(db: Session = Depends(get_session)) -> AuthService:
    """Get AuthService instance with database session."""
    return AuthService(db)


def get_user_service(db: Session = Depends(get_session)) -> UserService:
    """Get UserService instance with database session."""
    return UserService(db)


def get_watchlist_service(db: Session = Depends(get_session)) -> WatchlistService:
    """Get WatchlistService instance with database session."""
    return WatchlistService(db)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
WatchlistServiceDep = Annotated[WatchlistService, Depends(get_watchlist_service)]


# Health check dependencies
def get_health_check_info() -> HealthResponse:
    """Get application health check information."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=settings.environment,
        timestamp=time.time(),
        database=True,  # TODO: Add actual database health check
    )
