import { expect, test } from '@nuxt/test-utils/playwright';

test.describe('Home Page', () => {
  test('should load home page', async ({ page, goto }) => {
    await goto('/');
    await expect(page).toHaveTitle(/OtakuShelf/);
  });

  test('should display main content', async ({ page, goto }) => {
    await goto('/');
    // Check for main content elements
    await expect(page.locator('h1, h2, h3').first()).toBeVisible();
  });
});

test.describe('Navigation', () => {
  test('should navigate to about page', async ({ page, goto }) => {
    await goto('/about');
    await expect(page.locator('h1, h2').filter({ hasText: /about/i }).first()).toBeVisible();
  });

  test('should navigate to anime page', async ({ page, goto }) => {
    await goto('/anime');
    await expect(page).toHaveURL(/.*anime/);
  });
});
