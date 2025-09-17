"""
OtakuShelf Backend API
Production-ready FastAPI application with SuperTokens authentication.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from supertokens_python import (
    get_all_cors_headers,
    init,
    InputAppInfo,
    SupertokensConfig,
)
from supertokens_python.framework.fastapi import get_middleware as get_supertokens_middleware
from supertokens_python.recipe import emailpassword, session, dashboard

from .config import get_settings
from .db.core import create_db_and_tables
from .dependencies import (
    LoggingMiddleware,
    ErrorHandlingMiddleware,
)
from .routers import users_router, watchlist_router, health_router

# Load settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 Starting OtakuShelf API...")

    # Initialize database
    create_db_and_tables()
    print("✅ Database initialized")

    yield

    # Shutdown
    print("🛑 Shutting down OtakuShelf API...")


# Initialize SuperTokens
init(
    app_info=InputAppInfo(
        app_name=settings.app_name,
        api_domain=settings.api_domain,
        website_domain=settings.website_domain,
        api_base_path="/auth",
        website_base_path="/auth",
    ),
    supertokens_config=SupertokensConfig(
        connection_uri=settings.supertokens_connection_uri,
        api_key=settings.supertokens_api_key,
    ),
    framework="fastapi",
    recipe_list=[
        session.init(),  # Session management with default settings  
        emailpassword.init(),  # Email/password authentication
        dashboard.init(),  # SuperTokens dashboard
    ],
    mode="asgi",
)

# Create FastAPI app
app = FastAPI(
    title="OtakuShelf API",
    description="Anime watchlist management API",
    version="1.0.0",
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
    lifespan=lifespan,
)

# Add SuperTokens middleware (must be first)
app.add_middleware(get_supertokens_middleware())

# Add custom middleware
if settings.environment == "development":
    app.add_middleware(LoggingMiddleware)

app.add_middleware(ErrorHandlingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

# Include routers
app.include_router(users_router, prefix="/api/v1")
app.include_router(watchlist_router, prefix="/api/v1")
app.include_router(health_router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to OtakuShelf API",
        "version": "1.0.0",
        "docs": "/docs" if settings.environment != "production" else "disabled",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
        log_level=settings.log_level,
    )
