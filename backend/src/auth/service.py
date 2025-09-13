"""
Authentication service for bridging SuperTokens with our database.
Handles user creation and management.
"""

from typing import Optional

from sqlmodel import Session, select
from supertokens_python.recipe.emailpassword.asyncio import sign_up, sign_in
from supertokens_python.recipe.emailpassword.interfaces import (
    SignUpOkResult,
    SignInOkResult,
)

from ..models import User, UserCreate
from ..db.core import get_session


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self, db: Session):
        self.db = db

    async def create_user_from_supertokens(
        self,
        supertokens_user_id: str,
        email: str,
        username: str,
        full_name: Optional[str] = None,
    ) -> User:
        """
        Create a user in our database after SuperTokens signup.

        Args:
            supertokens_user_id: SuperTokens user ID
            email: User email
            username: Unique username
            full_name: Optional full name

        Returns:
            User: Created user object
        """
        user_data = UserCreate(
            supertokens_user_id=supertokens_user_id,
            username=username,
            email=email,
            full_name=full_name,
        )

        db_user = User.model_validate(user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def get_user_by_supertokens_id(self, supertokens_user_id: str) -> Optional[User]:
        """
        Get user by SuperTokens user ID.

        Args:
            supertokens_user_id: SuperTokens user ID

        Returns:
            User: User object if found, None otherwise
        """
        statement = select(User).where(User.supertokens_user_id == supertokens_user_id)
        return self.db.exec(statement).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username to search for

        Returns:
            User: User object if found, None otherwise
        """
        statement = select(User).where(User.username == username)
        return self.db.exec(statement).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: Email to search for

        Returns:
            User: User object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        return self.db.exec(statement).first()

    def is_username_available(self, username: str) -> bool:
        """
        Check if username is available.

        Args:
            username: Username to check

        Returns:
            bool: True if available, False otherwise
        """
        return self.get_user_by_username(username) is None

    async def signup_user(
        self, email: str, password: str, username: str, full_name: Optional[str] = None
    ) -> tuple[bool, str, Optional[User]]:
        """
        Sign up a new user with SuperTokens and create database record.

        Args:
            email: User email
            password: User password
            username: Unique username
            full_name: Optional full name

        Returns:
            tuple: (success, message, user_object)
        """
        # Check if username is available
        if not self.is_username_available(username):
            return False, "Username already taken", None

        # Check if email is already registered in our database
        if self.get_user_by_email(email):
            return False, "Email already registered", None

        # Sign up with SuperTokens
        result = await sign_up("public", email, password)

        if isinstance(result, SignUpOkResult):
            # Create user in our database
            try:
                user = await self.create_user_from_supertokens(
                    supertokens_user_id=result.user.id,
                    email=email,
                    username=username,
                    full_name=full_name,
                )
                return True, "User created successfully", user
            except Exception as e:
                return False, f"Failed to create user profile: {str(e)}", None
        else:
            return False, "Email already exists or invalid data", None

    async def signin_user(
        self, email: str, password: str
    ) -> tuple[bool, str, Optional[User]]:
        """
        Sign in user with SuperTokens and return user object.

        Args:
            email: User email
            password: User password

        Returns:
            tuple: (success, message, user_object)
        """
        result = await sign_in("public", email, password)

        if isinstance(result, SignInOkResult):
            user = self.get_user_by_supertokens_id(result.user.id)
            if user:
                return True, "Sign in successful", user
            else:
                return False, "User profile not found", None
        else:
            return False, "Invalid credentials", None


def get_auth_service(db: Session = next(get_session())) -> AuthService:
    """Dependency to get AuthService instance."""
    return AuthService(db)
