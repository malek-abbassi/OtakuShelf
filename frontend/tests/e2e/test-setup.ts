import { expect, test } from '@nuxt/test-utils/playwright';

type TestOptions = Parameters<Parameters<typeof test>[2]>[0];

type TestNavigationOptions = {
  page: TestOptions['page'];
  goto: TestOptions['goto'];
};

// Re-export the base test
export { expect, test };

// Test user credentials
const TEST_USER = {
  email: 'test@example.com',
  password: 'testpassword123',
  username: 'testuser',
  fullName: 'Test User',
};

// Authentication helper functions
export const authHelpers = {
  // Ensure test user is authenticated
  async authenticateUser({ page, goto }: TestNavigationOptions) {
    // First, check if already logged in
    let isLoggedIn = await this.checkUserLoggedIn({ page, goto });
    if (isLoggedIn)
      return;

    // sign in first to check if user exists
    isLoggedIn = await this.loginUser({ page, goto });
    if (isLoggedIn)
      return;

    // If login fails, sign up the user
    await this.signupUser({ page, goto });
  },

  // Check if user is logged in
  checkUserLoggedIn: async ({ page, goto }: TestNavigationOptions) => {
    await goto('/', { waitUntil: 'hydration' });
    await page.waitForLoadState('networkidle');

    // Check for an element that indicates the user is logged in
    const loggedInIndicator = page.locator('[data-testid="user-avatar"], [data-testid="logout-button"]').or(
      page.locator('button, a').filter({ hasText: /logout|sign out/i }),
    );
    return await loggedInIndicator.isVisible();
  },

  // Logout the current user
  async logoutUser(page: any) {
    // Try to find and click logout button
    const logoutButton = page.locator('[data-testid="logout-button"], button').filter({ hasText: /logout|sign out/i }).first();
    if (await logoutButton.isVisible()) {
      await logoutButton.click();
      await page.waitForLoadState('networkidle');
    }
    else {
      // Fallback: clear local storage and reload
      await page.evaluate(() => {
        localStorage.clear();
        sessionStorage.clear();
      });
      await page.reload();
      await page.waitForLoadState('networkidle');
    }
  },

  // Login with test user using normal UI flow
  async loginUser({ page, goto }: TestNavigationOptions) {
    // Now login with the test user
    await goto('/auth', { waitUntil: 'hydration' });
    await page.waitForLoadState('networkidle');

    // Make sure we're in sign in mode
    const signInToggle = page.locator('[data-testid="auth-toggle-mode"]').filter({ hasText: /sign in/i });
    if (await signInToggle.isVisible()) {
      await signInToggle.click();
    }

    // Fill login form
    const emailInput = page.locator('[data-testid="email-input"]');
    const passwordInput = page.locator('[data-testid="password-input"]');
    const signInButton = page.locator('[data-testid="auth-submit-button"]').filter({ hasText: /sign in/i });

    await emailInput.fill(TEST_USER.email);
    await passwordInput.fill(TEST_USER.password);
    await signInButton.click();

    // Wait for login to complete
    await page.waitForLoadState('networkidle');

    // Verify login was successful by checking if we can access protected page
    return await this.checkUserLoggedIn({ page, goto });
  },

  // Sign up user
  async signupUser({ page, goto }: TestNavigationOptions) {
    await goto('/auth', { waitUntil: 'hydration' });
    await page.waitForLoadState('networkidle');

    // Switch to sign up mode
    const signUpToggle = page.locator('[data-testid="auth-toggle-mode"]').filter({ hasText: /sign up/i });
    if (await signUpToggle.isVisible()) {
      await signUpToggle.click();
    }

    // Fill sign up form
    const emailInput = page.locator('[data-testid="email-input"]');
    const fullNameInput = page.locator('[data-testid="full-name-input"]');
    const passwordInput = page.locator('[data-testid="password-input"]');
    const signUpButton = page.locator('[data-testid="auth-submit-button"]').filter({ hasText: /sign up/i });

    await emailInput.fill(TEST_USER.email);
    await fullNameInput.fill(TEST_USER.fullName);
    await passwordInput.fill(TEST_USER.password);
    await signUpButton.click();

    // Wait for sign up to complete
    await page.waitForLoadState('networkidle');

    // Verify sign up was successful by checking if we can access protected page
    return await this.checkUserLoggedIn({ page, goto });
  },
  // Expect redirect to auth page when accessing protected route
  async expectAuthRedirect({ page }: TestNavigationOptions) {
    await expect(page).toHaveURL(/.*auth/);
    // Optionally check for auth form presence
    await expect(page.locator('form, [data-testid*="auth"]').first()).toBeVisible();
  },
};

// Test data helpers
export const testData = {
  mockUser: TEST_USER,

  mockAnime: {
    id: '1',
    title: { romaji: 'Test Anime', english: 'Test Anime English' },
    description: 'A test anime description',
    coverImage: { large: 'https://example.com/image.jpg' },
    status: 'FINISHED',
    episodes: 12,
    genres: ['Action', 'Adventure'],
  },
};
