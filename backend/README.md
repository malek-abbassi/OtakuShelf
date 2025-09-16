# OtakuShelf Backend

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![CI](https://github.com/malek-abbassi/OtakuShelf/actions/workflows/tests.yml/badge.svg)](https://github.com/malek-abbassi/OtakuShelf/actions/workflows/tests.yml)

The backend for OtakuShelf, a modern anime watchlist management system built with FastAPI, SQLModel, and SuperTokens authentication.

## 🚀 Features

### Core Functionality

- **RESTful API**: Complete REST API for anime watchlist management
- **User Authentication**: Secure authentication with SuperTokens
- **Database Integration**: PostgreSQL with SQLModel ORM
- **Data Validation**: Pydantic models for robust data validation
- **Health Monitoring**: Built-in health checks and monitoring
- **CORS Support**: Configurable CORS for frontend integration

### Technical Features

- **Async/Await**: Full async support with FastAPI
- **Auto Documentation**: Interactive API docs with Swagger/ReDoc
- **Environment Configuration**: Flexible configuration management
- **Database Migrations**: Automatic table creation and management
- **Testing Suite**: Comprehensive unit and integration tests
- **Docker Support**: Complete containerization

## 🏗️ Architecture

```bash
Backend Service
├── FastAPI Application
│   ├── Authentication (SuperTokens)
│   ├── User Management
│   ├── Watchlist Management
│   └── Health Monitoring
├── Database Layer
│   ├── PostgreSQL
│   ├── SQLModel ORM
│   └── Connection Pooling
└── External Services
    ├── AniList API (via Frontend)
    └── SuperTokens Auth Service
```

## 🛠️ Technology Stack

- **Framework**: FastAPI - Modern, fast web framework for building APIs
- **Database**: PostgreSQL - Robust relational database
- **ORM**: SQLModel - SQL databases in Python, designed for simplicity
- **Authentication**: SuperTokens - Secure, open-source authentication
- **Validation**: Pydantic - Data validation and settings management
- **Package Management**: uv - Fast Python package installer and resolver
- **Linting**: Ruff - Fast Python linter and formatter
- **Testing**: pytest - Feature-rich testing framework

## 📋 Prerequisites

- **Python 3.12+**
- **PostgreSQL 15+** (or Docker for local development)
- **uv** (Python package manager)
- **SuperTokens** instance (via Docker Compose)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

The easiest way to run the backend is with the root project's Docker Compose:

```bash
# From the project root
docker-compose up -d
```

### Option 2: Local Development

1. **Navigate to backend directory**

   ```bash
   cd backend
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the development server**

   ```bash
   uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

When the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/otaku_shelf

# SuperTokens Configuration
SUPERTOKENS_CONNECTION_URI=http://localhost:3567
SUPERTOKENS_API_KEY=your-api-key-here

# Application Settings
ENVIRONMENT=development
API_DOMAIN=http://localhost:8000
WEBSITE_DOMAIN=http://localhost:3000
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Logging
LOG_LEVEL=info
```

### Configuration Options

- **ENVIRONMENT**: `development`, `staging`, `production`
- **LOG_LEVEL**: `debug`, `info`, `warning`, `error`, `critical`
- **CORS_ORIGINS**: List of allowed origins for CORS

## 🧪 Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_user_model.py

# Run integration tests
uv run pytest tests/integration/
```

### Test Structure

```bash
tests/
├── unit/                    # Unit tests
│   ├── test_user_model.py
│   ├── test_watchlist_model.py
│   └── test_auth_service.py
├── integration/             # Integration tests
│   ├── test_users_api.py
│   └── test_watchlist_api.py
├── conftest.py             # Test configuration
└── factories/              # Test data factories
```

## 🛠️ Development

### Code Quality

```bash
# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Fix linting issues automatically
uv run ruff check . --fix
```

### Project Structure

```bash
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Application configuration
│   ├── dependencies.py      # Dependency injection
│   ├── schemas.py           # Pydantic schemas
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── service.py       # Authentication service
│   │   └── dependencies.py  # Auth dependencies
│   ├── db/
│   │   ├── __init__.py
│   │   ├── core.py          # Database connection and setup
│   │   └── models/          # Database models
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── watchlist.py     # Watchlist model
│   └── routers/
│       ├── __init__.py
│       ├── users.py         # User API routes
│       └── watchlist.py     # Watchlist API routes
├── tests/                   # Test suite
├── pyproject.toml           # Project configuration
├── Dockerfile               # Docker configuration
├── uv.lock                  # Dependency lock file
└── pytest.ini              # Test configuration
```

## 📡 API Endpoints

### Authentication

- `POST /auth/signup` - User registration
- `POST /auth/signin` - User login
- `POST /auth/signout` - User logout

### Users

- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile

### Watchlist

- `GET /api/v1/watchlist` - Get user's watchlist
- `POST /api/v1/watchlist` - Add anime to watchlist
- `GET /api/v1/watchlist/{id}` - Get specific watchlist item
- `PUT /api/v1/watchlist/{id}` - Update watchlist item
- `DELETE /api/v1/watchlist/{id}` - Remove from watchlist

### Health

- `GET /health` - Health check endpoint

## 🚀 Deployment

### Docker Deployment

```bash
# Build the image
docker build -t otaku-shelf-backend .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e SUPERTOKENS_CONNECTION_URI=http://... \
  otaku-shelf-backend
```

### Production Considerations

- Set `ENVIRONMENT=production` to disable debug features
- Use environment variables for all configuration
- Set up proper logging and monitoring
- Configure database connection pooling
- Use HTTPS in production
- Set up proper CORS policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation for API changes
- Use type hints for all function parameters
- Keep functions small and focused

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

#### Database Connection Error

- Ensure PostgreSQL is running
- Check DATABASE_URL configuration
- Verify database credentials

#### SuperTokens Connection Error

- Ensure SuperTokens service is running
- Check SUPERTOKENS_CONNECTION_URI
- Verify API key configuration

#### Port Already in Use

- Change the port in uvicorn command
- Kill existing processes on port 8000
- Use `lsof -i :8000` to find processes

### Debug Mode

Enable debug logging:

```bash
LOG_LEVEL=debug uv run uvicorn src.main:app --reload
```

## � CI/CD Pipeline

The backend uses GitHub Actions for automated testing and quality assurance. The CI pipeline runs on every push and pull request to ensure code quality and functionality.

### 🚀 Backend CI Checks

#### CI Code Quality

- **Linting**: Automated code style and quality checks with Ruff
- **Import Sorting**: Consistent import organization
- **Type Checking**: Python type hint validation

#### Testing Suite

- **Unit Tests**: Individual function and class testing with pytest
- **Integration Tests**: API endpoint and database interaction testing
- **Coverage Analysis**: Code coverage reporting with coverage.py
- **Test Results**: Detailed test output and failure analysis

#### Security & Dependencies

- **Dependency Scanning**: Security vulnerabilities in Python packages
- **License Compliance**: Open source license compatibility checks

### 📊 Quality Metrics

The CI pipeline enforces the following quality standards:

- ✅ **All tests must pass** (blocking requirement)
- ✅ **Code coverage minimum 80%** (recommended)
- ✅ **No critical security vulnerabilities** (blocking)
- ✅ **Linting standards met** (blocking)

### 🏃‍♂️ Local Development

Run the same checks locally before committing:

```bash
# Install test dependencies
uv sync --group test

# Run linting
uv run ruff check .

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test categories
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v
```

### 📈 Coverage Reports

Test coverage reports are automatically generated and can be viewed locally:

```bash
# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
# Open coverage/htmlcov/index.html in browser
```

## �📞 Support

For support and questions:

- Check the API documentation at `/docs`
- Review the main project README
- Open an issue on GitHub
- Check existing issues for similar problems

---

Built with ❤️ for anime enthusiasts
