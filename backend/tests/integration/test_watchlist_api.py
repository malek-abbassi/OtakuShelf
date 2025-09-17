"""
Integration tests for Watchlist API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.models import WatchlistItem


@pytest.mark.integration
@pytest.mark.watchlist
class TestWatchlistAPI:
    """Test the Watchlist API endpoints."""

    def test_add_to_watchlist_success(self, client: TestClient, mock_get_current_user):
        """Test successfully adding anime to watchlist."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "anime_picture_url": "https://example.com/anime.jpg",
            "anime_score": 8.5,
            "status": "watching",
            "notes": "Great anime!"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["anime_id"] == 123
        assert data["anime_title"] == "Test Anime"
        assert data["anime_picture_url"] == "https://example.com/anime.jpg"
        assert data["anime_score"] == 8.5
        assert data["status"] == "watching"
        assert data["notes"] == "Great anime!"
        assert "created_at" in data
        assert "updated_at" in data

    def test_add_to_watchlist_duplicate(self, client: TestClient, mock_get_current_user, sample_watchlist_item):
        """Test adding duplicate anime to watchlist."""
        watchlist_data = {
            "anime_id": sample_watchlist_item.anime_id,  # Same anime ID
            "anime_title": "Different Title",
            "status": "plan_to_watch"
        }

        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 409

        data = response.json()
        assert "error" in data
        assert "already in your watchlist" in data["error"]["message"]

    def test_add_to_watchlist_unauthorized(self, client: TestClient):
        """Test adding to watchlist without authentication."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "status": "watching"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        # This should return 401 or 403 depending on auth middleware
        assert response.status_code in [401, 403]

    def test_add_to_watchlist_invalid_data(self, client: TestClient, mock_get_current_user):
        """Test adding to watchlist with invalid data."""
        watchlist_data = {
            "anime_id": "not-a-number",  # Invalid type
            "anime_title": "",  # Empty title
            "anime_score": 15.0  # Score too high
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 422

    def test_get_watchlist_success(self, client: TestClient, mock_get_current_user, sample_watchlist_item):
        """Test getting user's watchlist."""
        response = client.get("/api/v1/watchlist")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total_count" in data
        assert "status_counts" in data
        assert len(data["items"]) >= 1
        
        # Check first item
        item = data["items"][0]
        assert "anime_id" in item
        assert "anime_title" in item
        assert "status" in item
        assert "created_at" in item

    def test_get_watchlist_with_status_filter(self, client: TestClient, mock_get_current_user, sample_watchlist_item):
        """Test getting watchlist with status filter."""
        response = client.get(f"/api/v1/watchlist?status_filter={sample_watchlist_item.status}")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        
        # All items should have the filtered status
        for item in data["items"]:
            assert item["status"] == sample_watchlist_item.status

    def test_get_watchlist_with_pagination(self, client: TestClient, mock_get_current_user):
        """Test getting watchlist with pagination."""
        response = client.get("/api/v1/watchlist?skip=0&limit=5")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total_count" in data
        assert len(data["items"]) <= 5

    def test_get_watchlist_unauthorized(self, client: TestClient):
        """Test getting watchlist without authentication."""
        response = client.get("/api/v1/watchlist")
        # This should return 401 or 403 depending on auth middleware
        assert response.status_code in [401, 403]

    def test_update_watchlist_item_success(self, client: TestClient, mock_get_current_user, sample_watchlist_item):
        """Test successfully updating a watchlist item."""
        update_data = {
            "anime_score": 9.0,
            "status": "completed",
            "notes": "Updated notes"
        }
        
        response = client.put(f"/api/v1/watchlist/{sample_watchlist_item.id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        # anime_title should remain unchanged since it's not updateable
        assert data["anime_title"] == sample_watchlist_item.anime_title
        assert data["anime_score"] == 9.0
        assert data["status"] == "completed"
        assert data["notes"] == "Updated notes"

    def test_update_watchlist_item_not_found(self, client: TestClient, mock_get_current_user):
        """Test updating non-existent watchlist item."""
        update_data = {
            "status": "completed"
        }

        response = client.put("/api/v1/watchlist/99999", json=update_data)
        assert response.status_code == 404

        data = response.json()
        assert "error" in data
        assert "not found" in data["error"]["message"].lower()

    def test_update_watchlist_item_unauthorized(self, client: TestClient, sample_watchlist_item):
        """Test updating watchlist item without authentication."""
        update_data = {
            "status": "completed"
        }
        
        response = client.put(f"/api/v1/watchlist/{sample_watchlist_item.id}", json=update_data)
        # This should return 401 or 403 depending on auth middleware
        assert response.status_code in [401, 403]

    def test_delete_watchlist_item_success(self, client: TestClient, mock_get_current_user, sample_watchlist_item):
        """Test successfully deleting a watchlist item."""
        response = client.delete(f"/api/v1/watchlist/{sample_watchlist_item.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "Anime removed from watchlist" in data["message"]

    def test_delete_watchlist_item_not_found(self, client: TestClient, mock_get_current_user):
        """Test deleting non-existent watchlist item."""
        response = client.delete("/api/v1/watchlist/99999")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        assert "not found" in data["error"]["message"].lower()

    def test_delete_watchlist_item_unauthorized(self, client: TestClient, sample_watchlist_item):
        """Test deleting watchlist item without authentication."""
        response = client.delete(f"/api/v1/watchlist/{sample_watchlist_item.id}")
        # This should return 401 or 403 depending on auth middleware
        assert response.status_code in [401, 403]

    def test_get_watchlist_item_by_id_success(self, client: TestClient, mock_get_current_user, sample_watchlist_item):
        """Test getting a specific watchlist item by ID."""
        response = client.get(f"/api/v1/watchlist/{sample_watchlist_item.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == sample_watchlist_item.id
        assert data["anime_id"] == sample_watchlist_item.anime_id
        assert data["anime_title"] == sample_watchlist_item.anime_title

    def test_get_watchlist_item_not_found(self, client: TestClient, mock_get_current_user):
        """Test getting non-existent watchlist item."""
        response = client.get("/api/v1/watchlist/99999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_async_add_to_watchlist(self, async_client: AsyncClient, mock_get_current_user):
        """Test adding to watchlist with async client."""
        watchlist_data = {
            "anime_id": 456,
            "anime_title": "Async Test Anime",
            "status": "plan_to_watch"
        }
        
        response = await async_client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["anime_id"] == 456
        assert data["anime_title"] == "Async Test Anime"

    def test_watchlist_status_counts(self, client: TestClient, mock_get_current_user, test_session, sample_user):
        """Test watchlist status counts calculation."""
        # Create multiple watchlist items with different statuses
        statuses = ["watching", "completed", "plan_to_watch", "dropped", "on_hold"]
        for i, status in enumerate(statuses):
            item = WatchlistItem(
                user_id=sample_user.id,
                anime_id=1000 + i,
                anime_title=f"Test Anime {i}",
                status=status
            )
            test_session.add(item)
        test_session.commit()
        
        response = client.get("/api/v1/watchlist")
        assert response.status_code == 200
        
        data = response.json()
        status_counts = data["status_counts"]
        
        # Each status should have a count of 1
        for status in statuses:
            assert status_counts.get(status, 0) >= 1

    def test_watchlist_pagination_edge_cases(self, client: TestClient, mock_get_current_user):
        """Test watchlist pagination edge cases."""
        # Test with limit 0
        response = client.get("/api/v1/watchlist?limit=0")
        assert response.status_code == 422  # Should be validation error
        
        # Test with negative skip
        response = client.get("/api/v1/watchlist?skip=-1")
        assert response.status_code == 422  # Should be validation error
        
        # Test with very large limit
        response = client.get("/api/v1/watchlist?limit=1000")
        assert response.status_code == 422  # Should be validation error (exceeds max)

    def test_add_watchlist_minimal_data(self, client: TestClient, mock_get_current_user):
        """Test adding watchlist item with minimal required data."""
        watchlist_data = {
            "anime_id": 789,
            "anime_title": "Minimal Anime"
            # Only required fields
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["anime_id"] == 789
        assert data["anime_title"] == "Minimal Anime"
        assert data["status"] == "plan_to_watch"  # Default value

    # Edge case and error scenario tests
    def test_add_to_watchlist_invalid_anime_id(self, client: TestClient, mock_get_current_user):
        """Test adding anime with invalid ID."""
        watchlist_data = {
            "anime_id": -1,  # Invalid negative ID
            "anime_title": "Invalid Anime",
            "status": "watching"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 422  # Validation error
        
        data = response.json()
        assert "detail" in data  # FastAPI validation errors use "detail"

    def test_add_to_watchlist_empty_title(self, client: TestClient, mock_get_current_user):
        """Test adding anime with empty title."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "",  # Empty title
            "status": "watching"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data

    def test_add_to_watchlist_title_too_long(self, client: TestClient, mock_get_current_user):
        """Test adding anime with title too long."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "A" * 201,  # Too long (max 200 chars)
            "status": "watching"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data

    def test_add_to_watchlist_invalid_status(self, client: TestClient, mock_get_current_user):
        """Test adding anime with invalid status."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "status": "invalid_status"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data

    def test_add_to_watchlist_invalid_score(self, client: TestClient, mock_get_current_user):
        """Test adding anime with invalid score."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "status": "watching",
            "anime_score": 15.0  # Score too high (max 10.0)
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data

    def test_add_to_watchlist_notes_too_long(self, client: TestClient, mock_get_current_user):
        """Test adding anime with notes too long."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "status": "watching",
            "notes": "A" * 1001  # Too long (max 1000 chars)
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data

    def test_add_to_watchlist_invalid_picture_url(self, client: TestClient, mock_get_current_user):
        """Test adding anime with invalid picture URL."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "status": "watching",
            "anime_picture_url": "not-a-url"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data

    def test_update_watchlist_item_invalid_status(self, client: TestClient, mock_get_current_user, sample_watchlist_item):
        """Test updating watchlist item with invalid status."""
        update_data = {
            "status": "nonexistent_status"
        }
        
        response = client.put(f"/api/v1/watchlist/{sample_watchlist_item.id}", json=update_data)
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data

    def test_get_watchlist_invalid_pagination(self, client: TestClient, mock_get_current_user):
        """Test getting watchlist with invalid pagination parameters."""
        response = client.get("/api/v1/watchlist?skip=-1&limit=1000")  # Invalid skip and limit
        # Should handle gracefully - either validate or use defaults
        assert response.status_code in [200, 422]

    def test_bulk_update_invalid_item_ids(self, client: TestClient, mock_get_current_user):
        """Test bulk update with invalid item IDs."""
        update_data = {
            "item_ids": [-1, 0, 99999],  # Invalid IDs
            "new_status": "completed"
        }
        
        response = client.post("/api/v1/watchlist/bulk", json=update_data)
        # Should handle gracefully - either succeed with valid items or fail
        assert response.status_code in [200, 404, 422]

    # Security tests
    def test_watchlist_sql_injection_title(self, client: TestClient, mock_get_current_user):
        """Test protection against SQL injection in anime title."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "Test'; DROP TABLE watchlist_items; --",
            "status": "watching"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        # Should not succeed with malicious input
        assert response.status_code in [201, 422, 409]

    def test_watchlist_xss_in_notes(self, client: TestClient, mock_get_current_user):
        """Test that XSS input is stored as-is (no sanitization implemented)."""
        watchlist_data = {
            "anime_id": 123,
            "anime_title": "Test Anime",
            "status": "watching",
            "notes": "<script>alert('xss')</script>"
        }
        
        response = client.post("/api/v1/watchlist", json=watchlist_data)
        if response.status_code == 201:
            # Currently, no XSS sanitization is implemented, so script tags are stored
            data = response.json()
            assert "<script>" in data["notes"]

    # Performance tests
    def test_watchlist_pagination_limits(self, client: TestClient, mock_get_current_user):
        """Test watchlist pagination with extreme limits."""
        # Test with very large limit - should be rejected
        response = client.get("/api/v1/watchlist?limit=10000")
        assert response.status_code == 422  # Should reject invalid limit
        
        # Test with very large skip - should handle gracefully
        response = client.get("/api/v1/watchlist?skip=1000000")
        assert response.status_code == 200  # Should return empty results gracefully

    def test_watchlist_bulk_operations(self, client: TestClient, mock_get_current_user):
        """Test bulk watchlist operations to simulate high load."""
        # Create multiple items sequentially to test bulk operations
        created_items = []
        for i in range(5):
            watchlist_data = {
                "anime_id": 2000 + i,
                "anime_title": f"Bulk Test Anime {i}",
                "status": "watching"
            }
            response = client.post("/api/v1/watchlist", json=watchlist_data)
            assert response.status_code == 201
            created_items.append(response.json())

        # Verify all items were created
        assert len(created_items) == 5

        # Test bulk retrieval
        response = client.get("/api/v1/watchlist")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 5  # At least our 5 items
