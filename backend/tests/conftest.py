"""
Test configuration and fixtures for the OtakuShelf backend tests.
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Add the src directory to the Python path
backend_path = Path(__file__).parent.parent
src_path = backend_path / "src"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(src_path))

# Now import the modules
import src.config as config
import src.db.core as db_core
import src.main as main
import src.models as models


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings() -> config.Settings:
    """Create test settings."""
    return config.Settings(
        environment="testing",
        app_name="OtakuShelf Test",
        api_domain="http://localhost:8000",
        website_domain="http://localhost:3000",
        database_url="sqlite:///test.db",
        supertokens_connection_uri="http://localhost:3567",
        supertokens_api_key="test-api-key",
        cors_origins=["http://localhost:3000"],
        log_level="debug",
    )


@pytest.fixture
def test_db():
    """Create a test database."""
    # Create a temporary file for the database
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    
    database_url = f"sqlite:///{temp_db.name}"
    
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    yield engine
    
    # Cleanup
    engine.dispose()
    os.unlink(temp_db.name)


@pytest.fixture
def test_session(test_db) -> Generator[Session, None, None]:
    """Create a test database session."""
    with Session(test_db) as session:
        yield session


@pytest.fixture
def override_get_session(test_session):
    """Override the get_session dependency."""
    def _override_get_session():
        yield test_session
    
    main.app.dependency_overrides[db_core.get_session] = _override_get_session
    yield
    main.app.dependency_overrides.clear()


@pytest.fixture
def override_settings(test_settings):
    """Override the get_settings dependency."""
    def _override_get_settings():
        return test_settings
    
    main.app.dependency_overrides[config.get_settings] = _override_get_settings
    yield
    main.app.dependency_overrides.clear()


@pytest.fixture
def client(override_get_session, override_settings) -> TestClient:
    """Create a test client."""
    return TestClient(main.app)


@pytest_asyncio.fixture
async def async_client(override_get_session, override_settings) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=main.app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "supertokens_user_id": "test-st-user-id-123",
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
    }


@pytest.fixture
def sample_user(test_session, sample_user_data) -> models.User:
    """Create a sample user in the test database."""
    user = models.User(**sample_user_data)
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def sample_watchlist_item_data():
    """Sample watchlist item data for testing."""
    return {
        "anime_id": 1,
        "anime_title": "Test Anime",
        "anime_picture_url": "https://example.com/anime.jpg",
        "anime_score": 8.5,
        "status": "watching",
        "notes": "Great anime!",
    }


@pytest.fixture
def sample_watchlist_item(test_session, sample_user, sample_watchlist_item_data) -> models.WatchlistItem:
    """Create a sample watchlist item in the test database."""
    watchlist_item = models.WatchlistItem(
        **sample_watchlist_item_data,
        user_id=sample_user.id
    )
    test_session.add(watchlist_item)
    test_session.commit()
    test_session.refresh(watchlist_item)
    return watchlist_item


@pytest.fixture
def mock_supertokens_signup(mocker):
    """Mock SuperTokens signup."""
    from supertokens_python.recipe.emailpassword.interfaces import SignUpOkResult
    
    mock_result = SignUpOkResult(
        user={
            "id": "test-st-user-id-123",
            "email": "test@example.com",
            "time_joined": 1234567890,
        }
    )
    
    return mocker.patch(
        "src.auth.service.sign_up",
        return_value=mock_result
    )


@pytest.fixture
def mock_supertokens_signin(mocker):
    """Mock SuperTokens signin."""
    from supertokens_python.recipe.emailpassword.interfaces import SignInOkResult
    
    mock_result = SignInOkResult(
        user={
            "id": "test-st-user-id-123",
            "email": "test@example.com",
            "time_joined": 1234567890,
        }
    )
    
    return mocker.patch(
        "src.auth.service.sign_in",
        return_value=mock_result
    )


@pytest.fixture
def authenticated_user_headers():
    """Headers for authenticated requests."""
    return {
        "Authorization": "Bearer mock-token",
        "Content-Type": "application/json",
    }


@pytest.fixture
def mock_get_current_user(mocker, sample_user):
    """Mock the get_current_user dependency."""
    mock = mocker.patch("src.routers.users.get_current_user")
    mock.return_value = sample_user
    
    # Also mock for watchlist router
    mocker.patch("src.routers.watchlist.get_current_user", return_value=sample_user)
    
    return mock
