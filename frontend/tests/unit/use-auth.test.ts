import { mockNuxtImport } from '@nuxt/test-utils/runtime';
import { beforeEach, describe, expect, it, vi } from 'vitest';

// Mock the runtime config
mockNuxtImport('useRuntimeConfig', () => {
  return () => ({
    public: {
      apiBaseUrl: 'http://localhost:8000',
    },
  });
});

// Mock the toast composable
mockNuxtImport('useToast', () => {
  return () => ({
    add: vi.fn(),
    remove: vi.fn(),
    clear: vi.fn(),
  });
});

describe('useAuth composable', () => {
  let useAuth: any;

  beforeEach(async () => {
    // Reset modules before each test
    vi.resetModules();

    // Mock fetch and $fetch
    globalThis.fetch = vi.fn();

    // Mock SuperTokens modules
    vi.doMock('supertokens-web-js', () => ({
      default: {
        init: vi.fn(),
      },
    }));

    vi.doMock('supertokens-web-js/recipe/emailpassword', () => ({
      default: {
        init: vi.fn(),
        signUp: vi.fn().mockResolvedValue({
          status: 'OK',
          user: {
            id: 'test-user-id',
            email: 'test@example.com',
          },
        }),
        signIn: vi.fn().mockResolvedValue({
          status: 'OK',
          user: {
            id: 'test-user-id',
            email: 'test@example.com',
          },
        }),
      },
    }));

    vi.doMock('supertokens-web-js/recipe/session', () => ({
      default: {
        init: vi.fn(),
        doesSessionExist: vi.fn().mockResolvedValue(true),
        signOut: vi.fn().mockResolvedValue(undefined),
      },
    }));

    // Import the composable after mocking
    const { useAuth: importedUseAuth } = await import('../../app/composables/use-auth');
    useAuth = importedUseAuth;
  });

  it('should initialize auth state correctly', () => {
    const auth = useAuth();

    expect(auth.isLoggedIn).toBeDefined();
    expect(auth.userProfile).toBeDefined();
    expect(auth.isLoading).toBeDefined();
  });

  it('should handle user profile fetching', async () => {
    // Mock successful session existence
    vi.doMock('supertokens-web-js/recipe/session', () => ({
      default: {
        init: vi.fn(),
        doesSessionExist: vi.fn().mockResolvedValue(true),
        signOut: vi.fn(),
        attemptRefreshingSession: vi.fn(),
      },
    }));

    // Mock successful API response
    globalThis.$fetch = vi.fn().mockResolvedValue({
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      full_name: 'Test User',
      is_active: true,
      created_at: '2023-01-01T00:00:00Z',
      watchlist_count: 5,
    });

    const auth = useAuth();
    const profile = await auth.fetchUserProfile();

    expect(profile).toEqual({
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      fullName: 'Test User',
      isActive: true,
      createdAt: '2023-01-01T00:00:00Z',
      watchlistCount: 5,
    });
  });

  it('should handle failed profile fetch', async () => {
    // Mock session existence but failed API response
    vi.doMock('supertokens-web-js/recipe/session', () => ({
      default: {
        init: vi.fn(),
        doesSessionExist: vi.fn().mockResolvedValue(true),
        signOut: vi.fn(),
        attemptRefreshingSession: vi.fn(),
      },
    }));

    // Mock failed API response
    globalThis.$fetch = vi.fn().mockRejectedValue({
      status: 401,
      statusText: 'Unauthorized',
    });

    const auth = useAuth();
    const profile = await auth.fetchUserProfile();

    expect(profile).toBeNull();
  });

  it('should handle sign up', async () => {
    const auth = useAuth();

    // Mock backend API response via $fetch
    (globalThis.$fetch as any).mockResolvedValue({
      message: 'User created successfully',
      data: { user_id: 1, username: 'newuser' },
    });

    const result = await auth.signUp({
      email: 'newuser@example.com',
      password: 'password123',
      username: 'newuser',
      fullName: 'New User',
    });

    expect(result.success).toBe(true);
  });

  it('should handle sign in', async () => {
    const auth = useAuth();

    // Mock backend API response via $fetch
    (globalThis.$fetch as any).mockResolvedValue({
      message: 'Sign in successful',
      data: { user_id: 1, username: 'testuser' },
    });

    const result = await auth.signIn({
      email: 'test@example.com',
      password: 'password123',
    });

    expect(result.success).toBe(true);
  });

  it('should handle sign out', async () => {
    const auth = useAuth();

    await auth.signOut();

    // Verify that session signOut was called
    const Session = await import('supertokens-web-js/recipe/session');
    expect(Session.default.signOut).toHaveBeenCalled();
  });

  it('should handle authentication check', async () => {
    const auth = useAuth();

    // Mock successful profile fetch
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: () => Promise.resolve({
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
        full_name: 'Test User',
        is_active: true,
        created_at: '2023-01-01T00:00:00Z',
        watchlist_count: 5,
      }),
    });

    await auth.checkAuth();

    expect(auth.isLoggedIn.value).toBe(true);
    expect(auth.userProfile.value).not.toBeNull();
  });

  it('should handle failed authentication check', async () => {
    const auth = useAuth();

    // Mock failed session check
    vi.doMock('supertokens-web-js/recipe/session', () => ({
      default: {
        init: vi.fn(),
        doesSessionExist: vi.fn().mockResolvedValue(false),
        signOut: vi.fn(),
      },
    }));

    // Mock $fetch to ensure it's not called
    globalThis.$fetch = vi.fn();

    await auth.checkAuth();

    expect(auth.isLoggedIn.value).toBe(false);
    expect(auth.userProfile.value).toBeNull();
  });
});
