"""
Unit tests for AuthService.
"""

import pytest
from sqlmodel import Session

from src.services.auth_service import AuthService, UsernameTakenError, UserProfileNotFoundError
from src.models import User


@pytest.mark.unit
@pytest.mark.auth
class TestAuthService:
    """Test the AuthService class."""

    def test_auth_service_initialization(self, test_session: Session):
        """Test AuthService initialization."""
        auth_service = AuthService(test_session)
        assert auth_service.db == test_session

    @pytest.mark.asyncio
    async def test_create_user_from_supertokens(self, test_session: Session):
        """Test creating a user from SuperTokens data."""
        auth_service = AuthService(test_session)
        
        user = await auth_service.create_user_from_supertokens(
            supertokens_user_id="st-user-123",
            email="test@example.com",
            username="testuser",
            full_name="Test User"
        )
        
        assert user.id is not None
        assert user.supertokens_user_id == "st-user-123"
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.full_name == "Test User"
        assert user.is_active is True

    def test_get_user_by_supertokens_id(self, test_session: Session, sample_user):
        """Test getting user by SuperTokens ID."""
        auth_service = AuthService(test_session)
        
        found_user = auth_service.get_user_by_supertokens_id(sample_user.supertokens_user_id)
        
        assert found_user is not None
        assert found_user.id == sample_user.id
        assert found_user.supertokens_user_id == sample_user.supertokens_user_id

    def test_get_user_by_supertokens_id_not_found(self, test_session: Session):
        """Test getting user by non-existent SuperTokens ID."""
        auth_service = AuthService(test_session)
        
        found_user = auth_service.get_user_by_supertokens_id("non-existent-id")
        
        assert found_user is None

    def test_get_user_by_username(self, test_session: Session, sample_user):
        """Test getting user by username."""
        auth_service = AuthService(test_session)
        
        found_user = auth_service.get_user_by_username(sample_user.username)
        
        assert found_user is not None
        assert found_user.id == sample_user.id
        assert found_user.username == sample_user.username

    def test_get_user_by_username_not_found(self, test_session: Session):
        """Test getting user by non-existent username."""
        auth_service = AuthService(test_session)
        
        found_user = auth_service.get_user_by_username("non-existent-user")
        
        assert found_user is None

    def test_get_user_by_email(self, test_session: Session, sample_user):
        """Test getting user by email."""
        auth_service = AuthService(test_session)
        
        found_user = auth_service.get_user_by_email(sample_user.email)
        
        assert found_user is not None
        assert found_user.id == sample_user.id
        assert found_user.email == sample_user.email

    def test_get_user_by_email_not_found(self, test_session: Session):
        """Test getting user by non-existent email."""
        auth_service = AuthService(test_session)
        
        found_user = auth_service.get_user_by_email("non-existent@example.com")
        
        assert found_user is None

    def test_is_username_available_true(self, test_session: Session):
        """Test username availability check when available."""
        auth_service = AuthService(test_session)
        
        is_available = auth_service.is_username_available("available-username")
        
        assert is_available is True

    def test_is_username_available_false(self, test_session: Session, sample_user):
        """Test username availability check when taken."""
        auth_service = AuthService(test_session)
        
        is_available = auth_service.is_username_available(sample_user.username)
        
        assert is_available is False

    @pytest.mark.asyncio
    async def test_signup_user_success(self, test_session: Session, mock_supertokens_signup):
        """Test successful user signup."""
        auth_service = AuthService(test_session)

        user = await auth_service.signup_user(
            email="newuser@example.com",
            password="password123",
            username="newuser",
            full_name="New User"
        )

        assert user is not None
        assert user.email == "newuser@example.com"
        assert user.username == "newuser"
        assert user.full_name == "New User"
        assert user.supertokens_user_id == "test-st-user-id-123"

    @pytest.mark.asyncio
    async def test_signup_user_username_taken(self, test_session: Session, sample_user):
        """Test user signup with taken username."""
        auth_service = AuthService(test_session)

        with pytest.raises(UsernameTakenError) as exc_info:
            await auth_service.signup_user(
                email="different@example.com",
                password="password123",
                username=sample_user.username,  # Taken username
                full_name="Different User"
            )

        assert exc_info.value.status_code == 409
        assert sample_user.username in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_signin_user_success(self, test_session: Session, sample_user, mock_supertokens_signin):
        """Test successful user signin."""
        auth_service = AuthService(test_session)

        user = await auth_service.signin_user(
            email=sample_user.email,
            password="password123"
        )

        assert user is not None
        assert user.id == sample_user.id

    @pytest.mark.asyncio
    async def test_signin_user_not_found(self, test_session: Session, mock_supertokens_signin):
        """Test user signin when user not found in our database."""
        auth_service = AuthService(test_session)

        with pytest.raises(UserProfileNotFoundError) as exc_info:
            await auth_service.signin_user(
                email="notfound@example.com",
                password="password123"
            )

        assert exc_info.value.status_code == 404
        assert "User profile not found" in str(exc_info.value)

    def test_multiple_users_creation(self, test_session: Session):
        """Test creating multiple users."""
        users_data = [
            {
                "supertokens_user_id": f"st-user-{i}",
                "email": f"user{i}@example.com",
                "username": f"user{i}",
                "full_name": f"User {i}"
            }
            for i in range(5)
        ]
        
        created_users = []
        for user_data in users_data:
            user = User(**user_data)
            test_session.add(user)
            created_users.append(user)
        
        test_session.commit()
        
        for i, user in enumerate(created_users):
            test_session.refresh(user)
            assert user.id is not None
            assert user.username == f"user{i}"
            assert user.email == f"user{i}@example.com"

    def test_case_insensitive_operations(self, test_session: Session):
        """Test case handling in username and email operations."""
        auth_service = AuthService(test_session)
        
        # Create user with lowercase email and username
        user = User(
            supertokens_user_id="test-case-user",
            email="test@example.com",
            username="testuser"
        )
        test_session.add(user)
        test_session.commit()
        
        # Test exact matches
        found_by_email = auth_service.get_user_by_email("test@example.com")
        found_by_username = auth_service.get_user_by_username("testuser")
        
        assert found_by_email is not None
        assert found_by_username is not None
        
        # Test case variations (should not find due to case sensitivity in SQLite)
        not_found_email = auth_service.get_user_by_email("TEST@EXAMPLE.COM")
        not_found_username = auth_service.get_user_by_username("TESTUSER")
        
        # Note: SQLite is case-sensitive by default for text comparisons
        assert not_found_email is None
        assert not_found_username is None
