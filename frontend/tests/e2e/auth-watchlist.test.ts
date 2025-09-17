import { expect, test } from '@nuxt/test-utils/playwright';

test.describe('Authentication', () => {
  test('should load auth page', async ({ page, goto }) => {
    await goto('/auth', { waitUntil: 'hydration' });
    await expect(page).toHaveURL(/.*auth/);
  });

  test('should display auth form elements', async ({ page, goto }) => {
    await goto('/auth', { waitUntil: 'hydration' });
    // Check for email input field
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    // Check for password input field
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
    // Check for submit button
    await expect(page.locator('[data-testid="auth-submit-button"]')).toBeVisible();
  });

  test('should display auth form title', async ({ page, goto }) => {
    await goto('/auth', { waitUntil: 'hydration' });
    // Check for the main auth page title
    await expect(page.locator('[data-testid="auth-page-header"] h1')).toHaveText('Welcome to OtakuShelf');
    // Check for form title (either sign in or sign up)
    await expect(page.locator('[data-testid="auth-form-header"] h2')).toBeVisible();
  });
});

test.describe('Watchlist', () => {
  test('should load watchlist page', async ({ page, goto }) => {
    await goto('/watchlist', { waitUntil: 'hydration' });
    await expect(page).toHaveURL(/.*watchlist/);
  });

  test('should display watchlist header', async ({ page, goto }) => {
    await goto('/watchlist', { waitUntil: 'hydration' });
    await expect(page.locator('[data-testid="watchlist-header"] h1')).toHaveText('My Watchlist');
  });

  test('should display watchlist content area', async ({ page, goto }) => {
    await goto('/watchlist', { waitUntil: 'hydration' });
    // Check for watchlist content container
    await expect(page.locator('[data-testid="watchlist-view"]')).toBeVisible();
  });
});

test.describe('User Settings', () => {
  test('should load user settings page', async ({ page, goto }) => {
    await goto('/settings', { waitUntil: 'hydration' });
    await expect(page).toHaveURL(/.*settings/);
  });

  test('should display settings elements', async ({ page, goto }) => {
    await goto('/settings', { waitUntil: 'hydration' });
    // Check for settings-related content
    await expect(page.locator('h1, h2').filter({ hasText: /settings|user/i }).first()).toBeVisible();
  });
});
