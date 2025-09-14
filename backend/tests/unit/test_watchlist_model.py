"""
Unit tests for WatchlistItem model.
"""

import pytest
from datetime import datetime
from sqlmodel import Session
from pydantic import ValidationError

from src.models import WatchlistItem, WatchlistItemCreate, WatchlistItemUpdate
from tests.factories import WatchlistItemFactory


@pytest.mark.unit
class TestWatchlistItemModel:
    """Test the WatchlistItem model."""

    def test_watchlist_item_creation(self, test_session: Session, sample_user):
        """Test creating a watchlist item."""
        item_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "anime_picture_url": "https://example.com/anime.jpg",
            "anime_score": 8.5,
            "status": "watching",
            "notes": "Great anime!",
            "user_id": sample_user.id,
        }
        
        item = WatchlistItem(**item_data)
        test_session.add(item)
        test_session.commit()
        test_session.refresh(item)
        
        assert item.id is not None
        assert item.anime_id == 123
        assert item.anime_title == "Test Anime"
        assert item.anime_picture_url == "https://example.com/anime.jpg"
        assert item.anime_score == 8.5
        assert item.status == "watching"
        assert item.notes == "Great anime!"
        assert item.user_id == sample_user.id
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)

    def test_watchlist_item_factory(self):
        """Test the WatchlistItemFactory."""
        item = WatchlistItemFactory()
        
        assert item.anime_id is not None
        assert item.anime_title is not None
        assert item.status in ["plan_to_watch", "watching", "completed", "dropped", "on_hold"]
        assert 1.0 <= item.anime_score <= 10.0

    def test_watchlist_item_create_schema(self):
        """Test the WatchlistItemCreate schema."""
        item_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "anime_picture_url": "https://example.com/anime.jpg",
            "anime_score": 8.5,
            "status": "watching",
            "notes": "Great anime!",
        }
        
        item_create = WatchlistItemCreate(**item_data)
        
        assert item_create.anime_id == 123
        assert item_create.anime_title == "Test Anime"
        assert item_create.anime_picture_url == "https://example.com/anime.jpg"
        assert item_create.anime_score == 8.5
        assert item_create.status == "watching"
        assert item_create.notes == "Great anime!"

    def test_watchlist_item_update_schema(self):
        """Test the WatchlistItemUpdate schema."""
        item_update = WatchlistItemUpdate(
            anime_title="Updated Anime",
            anime_score=9.0,
            status="completed"
        )
        
        assert item_update.anime_title == "Updated Anime"
        assert item_update.anime_score == 9.0
        assert item_update.status == "completed"
        assert item_update.notes is None

    def test_anime_score_constraints(self):
        """Test anime score validation constraints."""
        # Test valid scores
        valid_item = WatchlistItemCreate(
            anime_id=1,
            anime_title="Test",
            anime_score=8.5
        )
        assert valid_item.anime_score == 8.5
        
        # Test boundary values
        min_score = WatchlistItemCreate(
            anime_id=1,
            anime_title="Test",
            anime_score=0.0
        )
        assert min_score.anime_score == 0.0
        
        max_score = WatchlistItemCreate(
            anime_id=1,
            anime_title="Test",
            anime_score=10.0
        )
        assert max_score.anime_score == 10.0

    def test_required_fields(self):
        """Test that required fields are enforced."""
        with pytest.raises(ValueError):
            WatchlistItemCreate()  # Missing required fields

    def test_watchlist_item_relationship_with_user(self, test_session: Session, sample_user):
        """Test watchlist item relationship with user."""
        item = WatchlistItem(
            anime_id=123,
            anime_title="Test Anime",
            status="watching",
            user_id=sample_user.id
        )
        test_session.add(item)
        test_session.commit()
        test_session.refresh(item)
        
        assert item.user.id == sample_user.id
        assert item.user.username == sample_user.username

    def test_default_values(self):
        """Test default values for optional fields."""
        item = WatchlistItemCreate(
            anime_id=123,
            anime_title="Test Anime"
        )
        
        assert item.status == "plan_to_watch"
        assert item.anime_picture_url is None
        assert item.anime_score is None
        assert item.notes is None

    def test_notes_length_constraint(self):
        """Test notes field length constraint."""
        long_notes = "x" * 1001  # Exceeds max length
        
        # This should raise a validation error
        with pytest.raises(ValidationError) as exc_info:
            WatchlistItemCreate(
                anime_id=123,
                anime_title="Test Anime",
                notes=long_notes
            )
        
        assert "String should have at most 1000 characters" in str(exc_info.value)

    def test_anime_title_length_constraint(self):
        """Test anime title length constraint."""
        long_title = "x" * 201  # Exceeds max length
        
        # This should raise a validation error
        with pytest.raises(ValidationError) as exc_info:
            WatchlistItemCreate(
                anime_id=123,
                anime_title=long_title
            )
        
        assert "String should have at most 200 characters" in str(exc_info.value)
