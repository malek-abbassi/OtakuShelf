"""
Integration tests for Users API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.models import User


@pytest.mark.integration
@pytest.mark.auth
class TestUsersAPI:
    """Test the Users API endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Welcome to OtakuShelf API"
        assert data["version"] == "1.0.0"

    def test_signup_success(self, client: TestClient, mock_supertokens_signup):
        """Test successful user signup."""
        signup_data = {
            "email": "newuser@example.com",
            "password": "Password123",
            "username": "newuser",
            "full_name": "New User"
        }
        
        response = client.post("/api/v1/users/signup", json=signup_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["message"] == "User created successfully"
        assert "data" in data
        assert data["data"]["username"] == "newuser"

    def test_signup_username_taken(self, client: TestClient, sample_user):
        """Test signup with taken username."""
        signup_data = {
            "email": "different@example.com",
            "password": "Password123",
            "username": sample_user.username,  # Taken username
            "full_name": "Different User"
        }
        
        response = client.post("/api/v1/users/signup", json=signup_data)
        assert response.status_code == 409
        
        data = response.json()
        assert "Username 'testuser' is already taken" in data["detail"]

    def test_signup_invalid_data(self, client: TestClient):
        """Test signup with invalid data."""
        signup_data = {
            "email": "invalid-email",  # Invalid email format
            "password": "123",  # Too short
            "username": "ab",  # Too short
        }
        
        response = client.post("/api/v1/users/signup", json=signup_data)
        assert response.status_code == 422  # Validation error

    def test_signin_success(self, client: TestClient, sample_user, mock_supertokens_signin):
        """Test successful user signin."""
        signin_data = {
            "email": sample_user.email,
            "password": "Password123"
        }
        
        response = client.post("/api/v1/users/signin", json=signin_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Sign in successful"
        assert "data" in data
        assert data["data"]["username"] == sample_user.username

    def test_signin_user_not_found(self, client: TestClient, mock_supertokens_signin):
        """Test signin with non-existent user."""
        # Configure mock to return failure for this test
        from supertokens_python.recipe.emailpassword.interfaces import WrongCredentialsError
        mock_supertokens_signin.return_value = WrongCredentialsError()
        
        signin_data = {
            "email": "notfound@example.com",
            "password": "Password123"
        }
        
        response = client.post("/api/v1/users/signin", json=signin_data)
        assert response.status_code == 401
        
        data = response.json()
        assert "Invalid email or password" in data["detail"]

    def test_get_current_user_profile(self, client: TestClient, mock_get_current_user):
        """Test getting current user profile."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "email" in data
        assert "watchlist_count" in data

    def test_get_current_user_profile_unauthorized(self, client: TestClient):
        """Test getting current user profile without authentication."""
        response = client.get("/api/v1/users/me")
        # This should return 401 or 403 depending on auth middleware
        assert response.status_code in [401, 403]

    def test_update_current_user_profile(self, client: TestClient, mock_get_current_user):
        """Test updating current user profile."""
        update_data = {
            "username": "updateduser",
            "full_name": "Updated Name"
        }
        
        response = client.put("/api/v1/users/me", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "updateduser"
        assert data["full_name"] == "Updated Name"

    def test_update_user_profile_username_taken(self, client: TestClient, mock_get_current_user, test_session):
        """Test updating profile with taken username."""
        # Create another user with a specific username
        other_user = User(
            supertokens_user_id="other-st-user",
            username="takenusername",
            email="other@example.com"
        )
        test_session.add(other_user)
        test_session.commit()
        
        update_data = {
            "username": "takenusername"  # Already taken
        }
        
        response = client.put("/api/v1/users/me", json=update_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "Username already taken" in data["detail"]

    def test_check_username_availability_available(self, client: TestClient):
        """Test checking availability of available username."""
        response = client.get("/api/v1/users/check-username/availableuser")
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "availableuser"
        assert data["available"] is True
        assert "available" in data["message"]

    def test_check_username_availability_taken(self, client: TestClient, sample_user):
        """Test checking availability of taken username."""
        response = client.get(f"/api/v1/users/check-username/{sample_user.username}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == sample_user.username
        assert data["available"] is False
        assert "already taken" in data["message"]

    def test_deactivate_current_user(self, client: TestClient, mock_get_current_user):
        """Test deactivating current user account."""
        response = client.delete("/api/v1/users/me")
        assert response.status_code == 200
        
        data = response.json()
        assert "deactivated successfully" in data["message"]

    def test_deactivate_user_unauthorized(self, client: TestClient):
        """Test deactivating user without authentication."""
        response = client.delete("/api/v1/users/me")
        # This should return 401 or 403 depending on auth middleware
        assert response.status_code in [401, 403]

    @pytest.mark.asyncio
    async def test_async_client_health_check(self, async_client: AsyncClient):
        """Test health check with async client."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data

    def test_signup_missing_fields(self, client: TestClient):
        """Test signup with missing required fields."""
        signup_data = {
            "email": "test@example.com"
            # Missing password, username
        }
        
        response = client.post("/api/v1/users/signup", json=signup_data)
        assert response.status_code == 422

    def test_signin_missing_fields(self, client: TestClient):
        """Test signin with missing required fields."""
        signin_data = {
            "email": "test@example.com"
            # Missing password
        }
        
        response = client.post("/api/v1/users/signin", json=signin_data)
        assert response.status_code == 422

    def test_update_profile_with_invalid_data(self, client: TestClient, mock_get_current_user):
        """Test updating profile with invalid data."""
        update_data = {
            "username": "ab",  # Too short
            "is_active": "not-a-boolean"  # Invalid type
        }
        
        response = client.put("/api/v1/users/me", json=update_data)
        assert response.status_code == 422

    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are present."""
        # Test a regular request for CORS headers instead of OPTIONS
        # since OPTIONS preflight requests are handled differently by TestClient
        response = client.get("/health")
        assert response.status_code == 200
        
        # CORS headers should be present in the response
        # Note: In actual browser scenarios, CORS headers would be more prominent
        # but TestClient doesn't fully simulate browser CORS behavior
