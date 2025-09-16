import { expect, test } from '@nuxt/test-utils/playwright';

test.describe('Authentication', () => {
  test('should load auth page', async ({ page, goto }) => {
    await goto('/auth');
    await expect(page).toHaveURL(/.*auth/);
  });

  test('should display auth form elements', async ({ page, goto }) => {
    await goto('/auth');
    // Check for UInput email field
    await expect(page.locator('input[type="email"][placeholder*="email"]').first()).toBeVisible();
    // Check for UInput password field
    await expect(page.locator('input[type="password"], input[placeholder*="password"]').first()).toBeVisible();
    // Check for submit button
    await expect(page.locator('button[type="submit"], button').filter({ hasText: /sign|login/i }).first()).toBeVisible();
  });

  test('should display auth form title', async ({ page, goto }) => {
    await goto('/auth');
    // Check for the main auth page title
    await expect(page.locator('h1').filter({ hasText: 'Welcome to OtakuShelf' })).toBeVisible();
    // Check for form title (either sign in or sign up)
    await expect(page.locator('h2').filter({ hasText: /Welcome Back|Create Account/i }).first()).toBeVisible();
  });
});

test.describe('Watchlist', () => {
  test('should load watchlist page', async ({ page, goto }) => {
    await goto('/watchlist');
    await expect(page).toHaveURL(/.*watchlist/);
  });

  test('should display watchlist header', async ({ page, goto }) => {
    await goto('/watchlist');
    await expect(page.locator('h1, h2').filter({ hasText: /watchlist/i }).first()).toBeVisible();
  });

  test('should display watchlist content area', async ({ page, goto }) => {
    await goto('/watchlist');
    // Check for watchlist content container
    await expect(page.locator('.watchlist, [data-testid*="watchlist"], main').first()).toBeVisible();
  });
});

test.describe('User Profile', () => {
  test('should load user profile page', async ({ page, goto }) => {
    await goto('/profile');
    await expect(page).toHaveURL(/.*profile/);
  });

  test('should display profile elements', async ({ page, goto }) => {
    await goto('/profile');
    // Check for profile-related content
    await expect(page.locator('h1, h2').filter({ hasText: /profile|user/i }).first()).toBeVisible();
  });
});
