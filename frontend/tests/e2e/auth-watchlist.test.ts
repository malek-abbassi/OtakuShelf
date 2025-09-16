import { expect, test } from '@nuxt/test-utils/playwright';

test.describe('Authentication', () => {
  test('should load auth page', async ({ page, goto }) => {
    await goto('/auth');
    await expect(page).toHaveURL(/.*auth/);
  });

  test('should have auth form elements', async ({ page, goto }) => {
    await goto('/auth');
    // Check for common auth form elements
    const emailInput = page.locator('input[type="email"], input[name="email"]');
    const passwordInput = page.locator('input[type="password"], input[name="password"]');

    await expect(emailInput.or(passwordInput).first()).toBeVisible();
  });
});

test.describe('Watchlist', () => {
  test('should load watchlist page', async ({ page, goto }) => {
    await goto('/watchlist');
    await expect(page).toHaveURL(/.*watchlist/);
  });

  test('should display watchlist content', async ({ page, goto }) => {
    await goto('/watchlist');
    // Check for watchlist page header which is always present
    await expect(page.locator('h1').filter({ hasText: 'My Watchlist' })).toBeVisible();
  });
});
