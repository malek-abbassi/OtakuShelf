"""
Authentication dependencies for FastAPI.
Provides user authentication and authorization.
"""

from typing import Annotated, Optional
import logging

from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer

from ..db.core import get_session
from ..models import User
from .service import AuthService

logger = logging.getLogger(__name__)


async def get_current_user_id(
    session: SessionContainer = Depends(verify_session(anti_csrf_check=False)),
) -> str:
    """
    Get the current user's SuperTokens ID from the session.

    Args:
        session: SuperTokens session container

    Returns:
        str: SuperTokens user ID

    Raises:
        HTTPException: If session is invalid
    """
    return session.get_user_id()


async def get_current_user(
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_session)],
) -> User:
    """
    Get the current authenticated user from the database.

    Args:
        user_id: SuperTokens user ID
        db: Database session

    Returns:
        User: Current user object

    Raises:
        HTTPException: If user not found
    """
    auth_service = AuthService(db)
    user = auth_service.get_user_by_supertokens_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    return user


async def get_optional_current_user(
    db: Annotated[Session, Depends(get_session)],
    session: Optional[SessionContainer] = Depends(
        verify_session(session_required=False)
    ),
) -> Optional[User]:
    """
    Get the current user if authenticated, None otherwise.
    Useful for endpoints that work with or without authentication.

    Args:
        db: Database session
        session: Optional SuperTokens session

    Returns:
        Optional[User]: Current user if authenticated, None otherwise
    """
    if not session:
        return None

    auth_service = AuthService(db)
    user = auth_service.get_user_by_supertokens_id(session.get_user_id())

    return user if user and user.is_active else None
