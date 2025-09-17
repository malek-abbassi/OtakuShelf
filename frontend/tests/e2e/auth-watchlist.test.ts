import { authHelpers, expect, test } from './test-setup';

test.describe('Authentication', () => {
  test('should load auth page', async ({ page, goto }) => {
    await goto('/auth');
    await expect(page).toHaveURL(/.*auth/);
  });

  test('should display auth form elements', async ({ page, goto }) => {
    await goto('/auth');
    // Check for auth form elements
    await expect(page.locator('form, [data-testid*="auth"]').first()).toBeVisible();
  });

  test('should display auth form title', async ({ page, goto }) => {
    await goto('/auth');
    await expect(page.locator('h1, h2').filter({ hasText: /welcome|sign in|login/i }).first()).toBeVisible();
  });
});

test.describe('Watchlist', () => {
  test('should redirect to auth when accessing watchlist without authentication', async ({ page, goto }) => {
    await goto('/watchlist', { waitUntil: 'hydration' });
    await authHelpers.expectAuthRedirect({ page, goto });
  });

  test('should display watchlist header when authenticated', async ({ page, goto }) => {
    await authHelpers.authenticateUser({ page, goto });
    await goto('/watchlist', { waitUntil: 'hydration' });
    // First check if the watchlist view is loaded
    await expect(page.locator('[data-testid="watchlist-view"]')).toBeVisible();
    // Then check for the header
    await expect(page.locator('h1').filter({ hasText: /watchlist/i }).first()).toBeVisible();
  });

  test('should display watchlist content area when authenticated', async ({ page, goto }) => {
    await authHelpers.authenticateUser({ page, goto });
    await goto('/watchlist', { waitUntil: 'hydration' });
    // Check for watchlist content container
    await expect(page.locator('[data-testid="watchlist-view"]')).toBeVisible();
  });
});

test.describe('User Settings', () => {
  test('should redirect to auth when accessing settings without authentication', async ({ page, goto }) => {
    await goto('/settings', { waitUntil: 'hydration' });
    await authHelpers.expectAuthRedirect({ page, goto });
  });

  test('should display settings elements when authenticated', async ({ page, goto }) => {
    await authHelpers.authenticateUser({ page, goto });
    await goto('/settings', { waitUntil: 'hydration' });
    // Check for settings-related content
    await expect(page.locator('h1, h2').filter({ hasText: /settings|user/i }).first()).toBeVisible();
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
