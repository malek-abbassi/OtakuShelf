"""
Authentication service for bridging SuperTokens with our database.
Handles user creation and management.
"""

from typing import Optional
import logging

from sqlmodel import Session
from supertokens_python.recipe.emailpassword.asyncio import sign_up, sign_in
from supertokens_python.recipe.emailpassword.interfaces import (
    SignUpOkResult,
    SignInOkResult,
)

from ..models import User, UserCreate, UserUpdate
from .user_service import UserService

logger = logging.getLogger(__name__)


class AuthException(Exception):
    """Base exception for authentication errors."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UsernameTakenError(AuthException):
    """Exception raised when username is already taken."""

    def __init__(self, username: str):
        super().__init__(f"Username '{username}' is already taken", 409)


class EmailAlreadyRegisteredError(AuthException):
    """Exception raised when email is already registered."""

    def __init__(self, email: str):
        super().__init__(f"Email '{email}' is already registered", 409)


class InvalidCredentialsError(AuthException):
    """Exception raised when credentials are invalid."""

    def __init__(self):
        super().__init__("Invalid email or password", 401)


class UserProfileNotFoundError(AuthException):
    """Exception raised when user profile is not found in database."""

    def __init__(self, supertokens_user_id: str):
        super().__init__(f"User profile not found for SuperTokens ID: {supertokens_user_id}", 404)


class UserCreationError(AuthException):
    """Exception raised when user creation fails."""

    def __init__(self, email: str, reason: str):
        super().__init__(f"Failed to create user profile for {email}: {reason}", 500)


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

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

        return self.user_service.create_user(user_data)

    def get_user_by_supertokens_id(self, supertokens_user_id: str) -> Optional[User]:
        """Get user by SuperTokens user ID."""
        return self.user_service.get_user_by_supertokens_id(supertokens_user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.user_service.get_user_by_username(username)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.user_service.get_user_by_email(email)

    def is_username_available(self, username: str) -> bool:
        """Check if username is available."""
        return self.user_service.is_username_available(username)

    async def signup_user(
        self, email: str, password: str, username: str, full_name: Optional[str] = None
    ) -> User:
        """
        Sign up a new user with SuperTokens and create database record.

        Args:
            email: User email
            password: User password
            username: Unique username
            full_name: Optional full name

        Returns:
            User: Created user object

        Raises:
            UsernameTakenError: If username is already taken
            EmailAlreadyRegisteredError: If email is already registered
            UserCreationError: If user creation fails
        """
        # Check if username is available
        if not self.is_username_available(username):
            logger.warning(f"Signup attempt with taken username: {username}")
            raise UsernameTakenError(username)

        # Check if email is already registered in our database
        if self.get_user_by_email(email):
            logger.warning(f"Signup attempt with existing email: {email}")
            raise EmailAlreadyRegisteredError(email)

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
                logger.info(f"User signed up successfully: {email}")
                return user
            except Exception as e:
                logger.error(f"Failed to create user profile for {email}: {str(e)}")
                raise UserCreationError(email, str(e))
        else:
            logger.warning(f"SuperTokens signup failed for {email}")
            raise AuthException("Email already exists or invalid data", 400)

    async def signin_user(
        self, email: str, password: str
    ) -> User:
        """
        Sign in user with SuperTokens and return user object.

        Args:
            email: User email
            password: User password

        Returns:
            User: Authenticated user object

        Raises:
            InvalidCredentialsError: If credentials are invalid
            UserProfileNotFoundError: If user profile not found in database
        """
        result = await sign_in("public", email, password)

        if isinstance(result, SignInOkResult):
            user = self.get_user_by_supertokens_id(result.user.id)
            if user:
                return user
            else:
                raise UserProfileNotFoundError(result.user.id)
        else:
            raise InvalidCredentialsError()

    def get_or_create_user_from_supertokens(self, supertokens_user_id: str, email: str) -> User:
        """
        Get existing user or create new one from SuperTokens data.
        Useful for handling users that exist in SuperTokens but not in our database.

        Args:
            supertokens_user_id: SuperTokens user ID
            email: User email

        Returns:
            User: User object

        Raises:
            UserCreationError: If user creation fails
        """
        user = self.get_user_by_supertokens_id(supertokens_user_id)
        if user:
            return user

        # Try to extract username from email
        username = email.split('@')[0]
        if not self.is_username_available(username):
            # Append numbers until we find an available username
            counter = 1
            while not self.is_username_available(f"{username}{counter}"):
                counter += 1
            username = f"{username}{counter}"

        try:
            user_data = UserCreate(
                supertokens_user_id=supertokens_user_id,
                username=username,
                email=email,
            )
            return self.user_service.create_user(user_data)
        except Exception as e:
            logger.error(f"Failed to create user profile for {email}: {str(e)}")
            raise UserCreationError(email, str(e))

    def update_user_profile(self, user: User, updates: UserUpdate) -> User:
        """
        Update user profile information.

        Args:
            user: User to update
            updates: Update data

        Returns:
            User: Updated user object
        """
        return self.user_service.update_user(user, updates)

    def deactivate_user(self, user: User) -> None:
        """
        Deactivate a user account.

        Args:
            user: User to deactivate
        """
        user.deactivate()
        self.user_service.update_user(user, UserUpdate(is_active=False))

    def reactivate_user(self, user: User) -> None:
        """
        Reactivate a user account.

        Args:
            user: User to reactivate
        """
        user.reactivate()
        self.user_service.update_user(user, UserUpdate(is_active=True))
