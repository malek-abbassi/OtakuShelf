import { authHelpers, expect, test } from './test-setup';

test.describe('Home Page', () => {
  test('should load home page', async ({ page, goto }) => {
    await goto('/', { waitUntil: 'hydration' });
    await expect(page).toHaveTitle(/OtakuShelf/);
  });

  test('should display main content', async ({ page, goto }) => {
    await goto('/', { waitUntil: 'hydration' });
    // Check for main content elements
    await expect(page.locator('h1, h2, h3').first()).toBeVisible();
  });
});

test.describe('Navigation', () => {
  test('should navigate to about page', async ({ page, goto }) => {
    await goto('/about');
    await expect(page.locator('h1, h2').filter({ hasText: /about/i }).first()).toBeVisible();
  });

  test('should navigate to privacy page', async ({ page, goto }) => {
    await goto('/privacy');
    await expect(page.locator('h1, h2').filter({ hasText: /privacy/i }).first()).toBeVisible();
  });

  test('should navigate to terms page', async ({ page, goto }) => {
    await goto('/terms');
    await expect(page.locator('h1, h2').filter({ hasText: /terms/i }).first()).toBeVisible();
  });

  test('should redirect to auth when accessing settings without authentication', async ({ page, goto }) => {
    await goto('/settings', { waitUntil: 'hydration' });
    await authHelpers.expectAuthRedirect({ page, goto });
  });

  test('should navigate to anime page', async ({ page, goto }) => {
    await goto('/anime', { waitUntil: 'hydration' });
    await expect(page).toHaveURL(/.*anime/);
  });

  test('should have working header navigation', async ({ page, goto }) => {
    await goto('/', { waitUntil: 'hydration' });
    // Check that header navigation links are present
    await expect(page.locator('a[href="/"], a[href="/anime"]').first()).toBeVisible();
  });
});

test.describe('Authenticated Navigation', () => {
  test('should access settings page when authenticated', async ({ page, goto }) => {
    await authHelpers.authenticateUser({ page, goto });
    await goto('/settings', { waitUntil: 'hydration' });
    await expect(page.locator('h1, h2').filter({ hasText: /settings/i }).first()).toBeVisible();
  });

  test('should access watchlist page when authenticated', async ({ page, goto }) => {
    await authHelpers.authenticateUser({ page, goto });
    await goto('/watchlist', { waitUntil: 'hydration' });
    await expect(page.locator('[data-testid="watchlist-view"]')).toBeVisible();
  });
});
