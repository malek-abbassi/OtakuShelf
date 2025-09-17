"""
User service for handling user-related business logic.
"""

from typing import Optional
import logging

from sqlmodel import Session, select

from ..models import User, UserCreate, UserUpdate
from ..exceptions import UserNotFoundError, InactiveUserError, DatabaseError
from ..db.core import get_session

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID."""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFoundError(user_id=user_id)
        return user

    def get_user_by_supertokens_id(self, supertokens_user_id: str) -> Optional[User]:
        """Get user by SuperTokens ID."""
        statement = select(User).where(User.supertokens_user_id == supertokens_user_id)
        return self.db.exec(statement).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        statement = select(User).where(User.username == username)
        return self.db.exec(statement).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        return self.db.exec(statement).first()

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        try:
            user = User.model_validate(user_data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"Created user: {user.username}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create user: {str(e)}")
            raise DatabaseError(f"Failed to create user: {str(e)}", "create_user")

    def update_user(self, user: User, update_data: UserUpdate) -> User:
        """Update user information."""
        try:
            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(user, field, value)

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"Updated user: {user.username}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update user {user.id}: {str(e)}")
            raise DatabaseError(f"Failed to update user: {str(e)}", "update_user")

    def ensure_user_is_active(self, user: User) -> None:
        """Ensure user account is active."""
        if not user.is_active:
            raise InactiveUserError(user.id)

    def deactivate_user(self, user: User) -> User:
        """Deactivate a user account."""
        try:
            user.is_active = False
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"Deactivated user: {user.username}")
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to deactivate user {user.id}: {str(e)}")
            raise DatabaseError(f"Failed to deactivate user: {str(e)}", "deactivate_user")

    def is_username_available(self, username: str, exclude_user_id: Optional[int] = None) -> bool:
        """Check if username is available."""
        query = select(User).where(User.username == username)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        return self.db.exec(query).first() is None

    def get_user_profile_data(self, user: User) -> dict:
        """Get user profile data including computed fields."""
        # Count watchlist items
        watchlist_count = len(user.watchlist_items) if user.watchlist_items else 0

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "watchlist_count": watchlist_count,
        }


def get_user_service(db: Session = next(get_session())) -> UserService:
    """Dependency to get UserService instance."""
    return UserService(db)
