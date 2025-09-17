# OtakuShelf

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/malek-abbassi/OtakuShelf/actions/workflows/tests.yml/badge.svg)](https://github.com/malek-abbassi/OtakuShelf/actions/workflows/tests.yml)

OtakuShelf is a modern, full-stack web application designed for anime enthusiasts to discover, organize, and track their favorite anime series. Built with cutting-edge technologies, it provides a seamless experience for managing personal anime collections with advanced search capabilities powered by AniList's comprehensive database.

## ✨ Features

### 🎯 Core Functionality

- **Advanced Anime Search**: Search through thousands of anime titles with real-time results from AniList
- **Personal Watchlist**: Create and manage your personal anime collection
- **Progress Tracking**: Track your watching progress for each series
- **Detailed Anime Information**: Access comprehensive details including ratings, genres, studios, and more
- **User Authentication**: Secure user accounts with SuperTokens authentication
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### 🔧 Technical Features

- **RESTful API**: Well-documented API endpoints for all operations
- **Real-time Data**: Integration with AniList GraphQL API for up-to-date information
- **Database Integration**: PostgreSQL with SQLModel ORM for robust data management
- **Caching Layer**: Redis-backed caching system for improved performance
- **Rate Limiting**: Configurable rate limiting to prevent abuse
- **Modern UI**: Built with Nuxt.js and Nuxt UI for a polished user experience
- **Type Safety**: Full TypeScript support on frontend, Pydantic models on backend
- **Comprehensive Testing**: Unit, integration, performance, security, and E2E tests
- **Docker Support**: Complete containerization for easy deployment

## 🏗️ Architecture

```mermaid
graph TD
    A[Frontend<br/>Nuxt.js + Vue 3] --> B[Backend<br/>FastAPI + Python]
    B --> C[(Database<br/>PostgreSQL)]
    B --> D[SuperTokens<br/>Auth Service]
    B --> E[(Cache<br/>Redis)]
    A --> F[AniList API<br/>GraphQL]
    D --> C
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended for easiest setup)
- **Node.js 22+** (for frontend development)
- **Python 3.12** (for backend development)
- **pnpm** (for frontend package management)
- **uv** (for Python package management)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/malek-abbassi/OtakuShelf.git
   cd OtakuShelf
   ```

2. **Start all services**

   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs` or `http://localhost:8000/redoc`
   - SuperTokens Dashboard: `http://localhost:8000/auth/dashboard` (for user management)

### Option 2: Local Development Setup

#### Backend Setup

1. **Navigate to backend directory**

   ```bash
   cd backend
   ```

2. **Install Python dependencies**

   ```bash
   uv sync --all-groups # Install all dependencies including dev and test
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the backend server**

   ```bash
   uv run uvicorn src.main:app --host "localhost" --port "8000" --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install Node dependencies**

   ```bash
   pnpm install
   ```

3. **Start the development server**

   ```bash
   pnpm run dev
   ```

## 📋 Environment Configuration

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/otaku_shelf

# SuperTokens
SUPERTOKENS_CONNECTION_URI=http://localhost:3567
SUPERTOKENS_API_KEY=your-very-long-api-key-here # should be at least 20 characters long

# Application
ENVIRONMENT=development
API_DOMAIN=http://localhost:8000
WEBSITE_DOMAIN=http://localhost:3000
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (Runtime Config)

The frontend automatically detects the backend API location, but you can override it in production:

```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_DOMAIN=http://localhost:8000
NUXT_PUBLIC_WEBSITE_DOMAIN=http://localhost:3000
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
uv run pytest
```

### Frontend Tests

```bash
cd frontend
pnpm run test        # Unit tests
pnpm run test:e2e    # End-to-end tests
```

### Test Coverage

The project includes comprehensive testing across multiple dimensions:

- **Unit Tests**: Individual function and component testing
- **Integration Tests**: API endpoint and database interaction testing
- **Performance Tests**: Load testing and response time validation
- **Security Tests**: Vulnerability and injection attack prevention
- **E2E Tests**: Full user journey testing with Playwright

## 📚 API Documentation

When running the backend, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

- `GET /health` - Health check
- `POST /api/v1/users/signup` - User registration
- `POST /api/v1/users/login` - User authentication
- `GET /api/v1/watchlist` - Get user's watchlist
- `POST /api/v1/watchlist` - Add anime to watchlist
- `PUT /api/v1/watchlist/{id}` - Update watchlist item

## 🛠️ Development

### Code Quality

#### Backend

```bash
cd backend
uv run ruff check .          # Lint code
uv run ruff format .         # Format code
uv run pytest --cov=src      # Run tests with coverage
```

#### Frontend

```bash
cd frontend
pnpm run lint                # Lint and fix issues
pnpm run test:coverage       # Run tests with coverage
```

### Project Structure

```bash
OtakuShelf/
├── .github/
│   └── workflows/           # CI/CD pipelines
├── .vscode/
│   └── settings.json        # VS Code workspace settings
├── backend/                 # FastAPI backend service
│   ├── src/                 # Source code
│   │   ├── main.py          # FastAPI application
│   │   ├── config.py        # Configuration management
│   │   ├── cache.py         # Redis caching layer
│   │   ├── rate_limit.py    # Rate limiting
│   │   ├── models/          # Database models
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   └── auth/            # Authentication
│   ├── tests/               # Test suites
│   │   ├── unit/            # Unit tests
│   │   ├── integration/     # Integration tests
│   │   ├── performance/     # Performance tests
│   │   └── security/        # Security tests
│   ├── pyproject.toml       # Python dependencies
│   ├── Dockerfile           # Backend container
│   └── README.md            # Backend documentation
├── frontend/                # Nuxt.js frontend application
│   ├── app/                 # Nuxt application
│   │   ├── pages/           # File-based routing
│   │   ├── components/      # Vue components
│   │   ├── composables/     # Vue composables
│   │   └── layouts/         # Page layouts
│   ├── queries/             # GraphQL queries
│   ├── tests/               # Test suites
│   │   ├── unit/            # Unit tests
│   │   ├── integration/     # Integration tests
│   │   └── e2e/             # E2E tests
│   ├── package.json         # Node dependencies
│   ├── nuxt.config.ts       # Nuxt configuration
│   ├── Dockerfile           # Frontend container
│   └── README.md            # Frontend documentation
├── docker-compose.yml       # Multi-service orchestration
├── LICENSE                  # MIT License
└── README.md               # Project documentation
```

## 🚀 Deployment

### Production Docker Deployment

1. **Build and start services**

   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

2. **Scale services if needed**

   ```bash
   docker-compose up -d --scale backend=3
   ```

### Environment Variables for Production

Ensure these are set in your production environment:

- `ENVIRONMENT=production`
- `DATABASE_URL` - Production database URL
- `SUPERTOKENS_CONNECTION_URI` - Production SuperTokens instance
- Secure API keys and passwords

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow the existing code style
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The CI pipeline runs automatically on every push and pull request to the `main` and `develop` branches.

### 🚀 CI Checks

#### Backend CI Pipeline

- **Linting**: Code quality checks with Ruff
- **Unit Tests**: Comprehensive unit test coverage with pytest
- **Integration Tests**: API endpoint testing with httpx
- **Performance Tests**: Load testing and response time validation
- **Security Tests**: Vulnerability and injection attack prevention
- **Coverage**: Code coverage reporting with Codecov

#### Frontend CI Pipeline

- **Linting**: ESLint code quality checks
- **Unit Tests**: Component and utility testing with Vitest
- **E2E Tests**: End-to-end testing with Playwright
- **Coverage**: Test coverage reporting with Codecov

#### Security CI Pipeline

- **Vulnerability Scan**: Automated security scanning with Trivy
- **Dependency Audit**: Security vulnerabilities in dependencies
- **SARIF Reports**: Security findings uploaded to GitHub Security tab

### 📊 Quality Gates

The pipeline implements quality gates that must pass before code can be merged:

- ✅ **Backend tests must pass** (blocking)
- ✅ **Frontend tests must pass** (blocking)
- ✅ **Performance tests must pass** (blocking)
- ✅ **Security tests must pass** (blocking)
- ⚠️ **Security scan** (non-blocking, informational)

### 🏃‍♂️ Running Locally

To run the same checks locally before pushing:

```bash
# Backend checks
cd backend
uv run ruff check .
uv run pytest --cov=src

# Frontend checks
cd frontend
pnpm lint
pnpm test:coverage
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AniList** - For providing the comprehensive anime database
- **SuperTokens** - For secure authentication infrastructure
- **Nuxt.js** - For the excellent Vue.js framework
- **FastAPI** - For the modern Python web framework

## 📞 Support

If you have any questions or need help:

- Open an issue on GitHub
- Check the documentation in each service's README
- Review the API documentation at `/docs`

---

## Happy anime tracking! 🎬✨

Built with ❤️ by Malek
