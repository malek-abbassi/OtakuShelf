"""
Unit tests for User model.
"""

import pytest
import sys
from datetime import datetime
from pathlib import Path
from sqlmodel import Session

# Add the src directory to the Python path
backend_path = Path(__file__).parent.parent.parent
src_path = backend_path / "src"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(src_path))

import src.models as models
from tests.factories import UserFactory


@pytest.mark.unit
class TestUserModel:
    """Test the User model."""

    def test_user_creation(self, test_session: Session):
        """Test creating a user."""
        user_data = {
            "supertokens_user_id": "test-st-user-123",
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
        }
        
        user = models.User(**user_data)
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_factory(self):
        """Test the UserFactory."""
        user = UserFactory()
        
        assert user.supertokens_user_id is not None
        assert user.username is not None
        assert user.email is not None
        assert user.full_name is not None
        assert user.is_active is True

    def test_user_create_schema(self):
        """Test the UserCreate schema."""
        user_data = {
            "supertokens_user_id": "test-st-user-123",
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
        }
        
        user_create = models.UserCreate(**user_data)
        
        assert user_create.supertokens_user_id == "test-st-user-123"
        assert user_create.username == "testuser"
        assert user_create.email == "test@example.com"
        assert user_create.full_name == "Test User"
        assert user_create.is_active is True

    def test_user_update_schema(self):
        """Test the UserUpdate schema."""
        user_update = models.UserUpdate(username="newusername", full_name="New Name")
        
        assert user_update.username == "newusername"
        assert user_update.full_name == "New Name"
        assert user_update.is_active is None

    def test_user_username_constraints(self):
        """Test username validation constraints."""
        # Test minimum length
        with pytest.raises(ValueError):
            models.UserCreate(
                supertokens_user_id="test-123",
                username="ab",  # Too short
                email="test@example.com"
            )

    def test_user_unique_constraints(self, test_session: Session):
        """Test unique constraints on username and email."""
        user1 = models.User(
            supertokens_user_id="test-st-user-1",
            username="testuser",
            email="test@example.com"
        )
        test_session.add(user1)
        test_session.commit()
        
        # Try to create another user with same username
        user2 = models.User(
            supertokens_user_id="test-st-user-2",
            username="testuser",  # Same username
            email="test2@example.com"
        )
        test_session.add(user2)
        
        with pytest.raises(Exception):  # Should raise integrity error
            test_session.commit()

    def test_user_relationship_with_watchlist(self, test_session: Session, sample_user):
        """Test user relationship with watchlist items."""
        # Create a watchlist item for the user
        watchlist_item = models.WatchlistItem(
            user_id=sample_user.id,
            anime_id=1,
            anime_title="Test Anime",
            status="watching"
        )
        test_session.add(watchlist_item)
        test_session.commit()
        test_session.refresh(sample_user)
        
        assert len(sample_user.watchlist_items) == 1
        assert sample_user.watchlist_items[0].anime_title == "Test Anime"
