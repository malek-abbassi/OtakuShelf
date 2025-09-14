// Test setup for Nuxt 4 with @nuxt/test-utils
import { mockNuxtImport } from '@nuxt/test-utils/runtime';
import { beforeAll, beforeEach, vi } from 'vitest';

// Global test setup
beforeAll(async () => {
  // Any global setup can go here
});

// Mock Nuxt composables using built-in utilities
mockNuxtImport('useRuntimeConfig', () => {
  return () => ({
    app: {
      baseURL: '/',
      buildAssetsDir: '/_nuxt/',
      cdnURL: undefined,
    },
    public: {
      apiBaseUrl: 'http://localhost:8000',
    },
  });
});

// Mock external APIs and services
vi.mock('~/composables/use-ani-list', () => ({
  useAniList: () => ({
    searchAnime: vi.fn().mockResolvedValue({
      data: {
        Page: {
          media: [
            {
              id: 1,
              title: { english: 'Test Anime', romaji: 'Test Anime' },
              coverImage: { large: 'https://example.com/image.jpg' },
              averageScore: 85,
              status: 'FINISHED',
              episodes: 12,
            },
          ],
          pageInfo: {
            hasNextPage: false,
            currentPage: 1,
            lastPage: 1,
            perPage: 20,
            total: 1,
          },
        },
      },
    }),
    getAnimeDetails: vi.fn().mockResolvedValue({
      data: {
        Media: {
          id: 1,
          title: { english: 'Test Anime', romaji: 'Test Anime' },
          description: 'Test description',
          coverImage: { large: 'https://example.com/image.jpg' },
          averageScore: 85,
          status: 'FINISHED',
          episodes: 12,
          genres: ['Action', 'Adventure'],
        },
      },
    }),
  }),
}));

// Mock Supertokens
vi.mock('supertokens-web-js', () => ({
  default: {
    init: vi.fn(),
  },
}));

vi.mock('supertokens-web-js/recipe/emailpassword', () => ({
  default: {
    init: vi.fn(),
    signUp: vi.fn(),
    signIn: vi.fn(),
  },
}));

vi.mock('supertokens-web-js/recipe/session', () => ({
  default: {
    init: vi.fn(),
    doesSessionExist: vi.fn().mockResolvedValue(true),
    signOut: vi.fn(),
  },
}));

// Mock fetch for API calls
globalThis.fetch = vi.fn() as any;
globalThis.$fetch = vi.fn() as any;

// Setup default fetch responses
beforeEach(() => {
  // Reset mocks before each test
  vi.clearAllMocks();

  // Setup default successful responses
  (globalThis.fetch as any).mockResolvedValue({
    ok: true,
    status: 200,
    json: () => Promise.resolve({}),
    text: () => Promise.resolve(''),
  });

  // Setup default $fetch responses
  (globalThis.$fetch as any).mockResolvedValue({});
});
