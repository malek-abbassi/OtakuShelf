# OtakuShelf Frontend

[![Nuxt.js](https://img.shields.io/badge/Nuxt-4.1+-00DC82.svg)](https://nuxt.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.5+-4FC08D.svg)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6+-3178C6.svg)](https://typescriptlang.org/)
[![CI](https://github.com/malek-abbassi/OtakuShelf/actions/workflows/tests.yml/badge.svg)](https://github.com/malek-abbassi/OtakuShelf/actions/workflows/tests.yml)

The frontend for OtakuShelf, a modern, responsive web application for anime discovery and watchlist management. Built with Nuxt.js 4, Vue 3, and TypeScript for optimal performance and developer experience.

## ✨ Features

### 🎨 User Interface

- **Modern Design**: Clean, responsive UI built with Nuxt UI and Tailwind CSS
- **Dark/Light Mode**: Automatic theme switching based on user preference
- **Mobile-First**: Fully responsive design for all device sizes
- **Accessibility**: WCAG compliant components and navigation
- **SEO Optimized**: Server-side rendering with meta tags and structured data

### 🚀 Core Functionality

- **Anime Search**: Real-time search powered by AniList GraphQL API
- **Detailed Anime Pages**: Comprehensive anime information and metadata
- **Personal Watchlist**: Create and manage your anime collection
- **Progress Tracking**: Track watching progress for each series
- **User Authentication**: Secure login/signup with SuperTokens
- **Profile Management**: User profile and preferences

### 🔧 Technical Features

- **Server-Side Rendering**: Fast initial page loads with Nuxt SSR
- **Static Generation**: Pre-rendered pages for optimal performance
- **Type Safety**: Full TypeScript support throughout the application
- **Component Library**: Consistent UI with Nuxt UI components
- **GraphQL Integration**: Efficient data fetching with GraphQL
- **State Management**: Reactive state with Vue 3 Composition API
- **Testing Suite**: Unit and E2E tests with Vitest and Playwright

## 🏗️ Architecture

```bash
Frontend Application (Nuxt.js)
├── Pages (File-based routing)
│   ├── / (Homepage - Anime Discovery)
│   ├── /anime/[id] (Anime Details)
│   ├── /watchlist (User Watchlist)
│   ├── /auth (Authentication)
│   └── /settings (User Settings)
├── Components
│   ├── UI Components (Nuxt UI)
│   ├── Anime Components
│   ├── Auth Components
│   └── Layout Components
├── Composables
│   ├── useAuth (Authentication)
│   ├── useAniList (Anime API)
│   ├── useWatchlist (Watchlist Management)
│   └── useAnimeUtils (Helper Functions)
├── API Integration
│   ├── GraphQL Queries (AniList)
│   ├── REST API (Backend)
│   └── Authentication (SuperTokens)
└── Assets & Styling
    ├── Tailwind CSS
    ├── Custom Components
    └── Static Assets
```

## 🛠️ Technology Stack

- **Framework**: Nuxt.js 4 - The progressive Vue.js framework
- **Language**: TypeScript - Type-safe JavaScript
- **UI Library**: Nuxt UI - Vue components built on Tailwind CSS
- **Styling**: Tailwind CSS 4 - Utility-first CSS framework
- **State Management**: Vue 3 Composition API - Reactive state management
- **GraphQL Client**: GraphQL Request - Lightweight GraphQL client
- **Authentication**: SuperTokens Web JS - Secure authentication
- **Package Manager**: pnpm - Fast, disk-efficient package manager
- **Testing**: Vitest + Playwright - Unit and E2E testing
- **Linting**: ESLint - Code quality and consistency

## 📋 Prerequisites

- **Node.js 22+**
- **pnpm** (recommended) or npm/yarn
- **Backend API** running (for full functionality)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

The easiest way to run the frontend is with the root project's Docker Compose:

```bash
# From the project root
docker-compose up -d
```

### Option 2: Local Development

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   pnpm install
   ```

3. **Start the development server**

   ```bash
   pnpm run dev
   ```

The application will be available at `http://localhost:3000`

## 📚 Key Pages & Features

### 🎬 Anime Search (`/anime`)

- **Anime Discovery**: Browse trending and popular anime
- **Search Functionality**: Real-time search with AniList integration
- **Comprehensive Information**: Title, description, ratings, studios
- **Visual Media**: Cover images, banners, and trailers
- **Metadata**: Episodes, duration, genres, tags
- **Watchlist Integration**: Add/remove from personal watchlist

### 📋 Watchlist (`/watchlist`)

- **Personal Collection**: View all saved anime
- **Progress Tracking**: Mark episodes watched
- **Status Management**: Plan to watch, watching, completed

### 🔐 Authentication (`/auth`)

- **Secure Login**: Email/password authentication
- **User Registration**: Create new accounts
- **Session Management**: Automatic session handling
- **Profile Management**: Update user information

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
# API Configuration
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_DOMAIN=http://localhost:8000
NUXT_PUBLIC_WEBSITE_DOMAIN=http://localhost:3000

# Application Settings
NODE_ENV=development
PORT=3000
```

### Runtime Configuration

The application uses Nuxt's runtime config for dynamic configuration:

```typescript
// nuxt.config.ts
runtimeConfig: {
  public: {
    apiBaseUrl: 'http://localhost:8000',
    apiDomain: 'http://localhost:8000',
    websiteDomain: 'http://localhost:3000',
  },
};
```

## 🧪 Testing

### Unit Tests

```bash
# Run unit tests
pnpm run test

# Run with coverage
pnpm run test:coverage

# Run in watch mode
pnpm run test:ui
```

### End-to-End Tests

```bash
# Run E2E tests
pnpm run test:e2e

# Run E2E tests with UI
pnpm run test:e2e:ui

# Run tests in specific browser
pnpm run test:e2e -- --project=chromium
```

### Test Structure

```bash
tests/
├── unit/                    # Unit tests
│   ├── components/          # Component tests
│   ├── composables/         # Composable tests
│   └── utils/               # Utility tests
└── integration/             # E2E tests
    ├── auth.spec.ts         # Authentication tests
    ├── search.spec.ts       # Search functionality
    └── watchlist.spec.ts    # Watchlist tests
```

## 🛠️ Development

### Code Quality

```bash
# Lint code
pnpm run lint

# Fix linting issues automatically
pnpm run lint:fix
```

### Project Structure

```bash
frontend/
├── app/
│   ├── app.vue              # Root component
│   ├── app.config.ts        # App configuration
│   ├── pages/               # File-based routing
│   │   ├── index.vue        # Homepage
│   │   ├── anime/
│   │   │   └── [id].vue     # Dynamic anime page
│   │   ├── watchlist.vue    # Watchlist page
│   │   ├── auth.vue         # Authentication page
│   │   └── settings.vue     # Settings page
│   ├── components/          # Vue components
│   │   ├── anime-card.vue   # Anime card component
│   │   ├── anime-search-enhanced.vue
│   │   ├── auth-form.vue    # Authentication form
│   │   ├── watchlist-card.vue
│   │   └── ui/              # Reusable UI components
│   ├── composables/         # Vue composables
│   │   ├── use-auth.ts      # Authentication logic
│   │   ├── use-ani-list.ts  # AniList API integration
│   │   ├── use-watchlist.ts # Watchlist management
│   │   └── use-anime-utils.ts
│   ├── layouts/             # Page layouts
│   │   └── default.vue      # Default layout
│   ├── middleware/          # Route middleware
│   └── types/               # TypeScript types
├── queries/                 # GraphQL queries
│   ├── anime.ts             # Anime-related queries
│   └── user.ts              # User-related queries
├── public/                  # Static assets
├── server/                  # Server-side code
├── types/                   # Global type definitions
├── package.json             # Dependencies and scripts
├── nuxt.config.ts           # Nuxt configuration
├── tailwind.config.js       # Tailwind configuration
├── vitest.config.ts         # Test configuration
├── playwright.config.ts     # E2E test configuration
└── eslint.config.mjs        # Linting configuration
```

## 🎨 Styling & Theming

### Tailwind CSS Configuration

The application uses Tailwind CSS 4 with custom configuration:

```javascript
// tailwind.config.js
export default {
  content: [
    './app/**/*.{vue,ts,js}',
    './nuxt.config.ts'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#64748b',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

### Nuxt UI Components

Built on top of Tailwind CSS with consistent theming:

- **UButton**: Styled buttons with variants
- **UInput**: Form inputs with validation
- **UCard**: Content containers
- **UModal**: Modal dialogs
- **UTable**: Data tables
- **UPagination**: Pagination controls

## 🚀 Deployment

### Build for Production

```bash
# Build the application
pnpm run build

# Preview production build
pnpm run preview

# Generate static site
pnpm run generate
```

### Docker Deployment

```bash
# Build Docker image
docker build -t otaku-shelf-frontend .

# Run container
docker run -p 3000:3000 \
  -e NUXT_PUBLIC_API_BASE_URL=http://your-api-url \
  otaku-shelf-frontend
```

### Environment Variables for Production

```env
NODE_ENV=production
NUXT_PUBLIC_API_BASE_URL=https://your-api-domain.com
NUXT_PUBLIC_API_DOMAIN=https://your-api-domain.com
NUXT_PUBLIC_WEBSITE_DOMAIN=https://your-frontend-domain.com
```

## 🔍 SEO & Performance

### SEO Features

- **Server-Side Rendering**: Fast initial page loads
- **Meta Tags**: Dynamic meta tags for each page
- **Structured Data**: JSON-LD for search engines
- **Open Graph**: Social media sharing optimization
- **Canonical URLs**: Prevent duplicate content issues

### Performance Optimizations

- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Nuxt Image with WebP/AVIF support
- **Caching**: HTTP caching headers and service worker
- **Lazy Loading**: Components and routes loaded on demand
- **Bundle Analysis**: Webpack bundle analyzer integration

### Development Guidelines

- Follow Vue 3 Composition API patterns
- Use TypeScript for all new code
- Write comprehensive tests
- Follow Nuxt.js best practices
- Maintain consistent code style
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

#### Build Errors

- Clear node_modules: `rm -rf node_modules && pnpm install`
- Clear Nuxt cache: `rm -rf .nuxt`
- Check Node.js version compatibility

#### API Connection Issues

- Verify backend API is running
- Check environment variables
- Review network configuration

#### Authentication Problems

- Ensure SuperTokens service is running
- Check API key configuration
- Verify CORS settings

### Debug Mode

Enable debug logging in development:

````bash
```bash
DEBUG=nuxt:* pnpm run dev
````

## 🔄 CI/CD Pipeline

The frontend uses GitHub Actions for automated testing, building, and quality assurance. The CI pipeline ensures code quality and prevents regressions.

### 🚀 Frontend CI Checks

#### CI Code Quality

- **ESLint**: Automated JavaScript/TypeScript linting and style checks
- **TypeScript**: Type checking and compilation validation
- **Import Sorting**: Consistent import organization

#### Testing Suite

- **Unit Tests**: Component and composable testing with Vitest
- **Integration Tests**: Component interaction and routing tests
- **E2E Tests**: End-to-end user journey testing with Playwright
- **Coverage Analysis**: Test coverage reporting and analysis

#### Build & Performance

- **Build Validation**: Ensures production builds complete successfully
- **Bundle Analysis**: Bundle size and optimization checks
- **Performance Metrics**: Lighthouse performance scoring

### 📊 Quality Standards

The CI pipeline enforces these quality requirements:

- ✅ **All tests must pass** (blocking requirement)
- ✅ **ESLint rules must pass** (blocking)
- ✅ **TypeScript compilation successful** (blocking)
- ✅ **Build process completes** (blocking)
- 📈 **Test coverage above 70%** (recommended)

### 🏃‍♂️ Local Development

Run the same checks locally before committing:

```bash
# Install dependencies
pnpm install

# Run linting
pnpm lint

# Run unit tests with coverage
pnpm test:coverage

# Run E2E tests
pnpm test:e2e

# Build for production
pnpm build
```

### 📈 Test Coverage

View detailed test coverage reports:

```bash
# Run tests with coverage
pnpm test:coverage

# Coverage report will be available in coverage/ directory
# Open coverage/index.html in browser
```

### 🎭 E2E Testing

End-to-end tests cover critical user journeys:

```bash
# Run E2E tests in headed mode (visible browser)
pnpm test:e2e:ui

# Run specific test file
pnpm test:e2e -- tests/e2e/auth.spec.ts

# Run tests in specific browser
pnpm test:e2e -- --project=chromium
```

---

Built with ❤️ by Malek
