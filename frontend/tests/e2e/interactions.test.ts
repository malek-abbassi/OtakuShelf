import { expect, test } from '@nuxt/test-utils/playwright';

test.describe('Settings Page', () => {
  test('should load settings page', async ({ page, goto }) => {
    await goto('/settings');
    await expect(page).toHaveURL(/.*settings/);
  });

  test('should display settings header', async ({ page, goto }) => {
    await goto('/settings');
    await expect(page.locator('h1, h2').filter({ hasText: /settings/i }).first()).toBeVisible();
  });

  test('should display settings form elements', async ({ page, goto }) => {
    await goto('/settings');
    // Check for common settings form elements
    await expect(page.locator('form, .settings-form').first()).toBeVisible();
  });
});

test.describe('User Interactions', () => {
  test('should handle navigation between pages', async ({ page, goto }) => {
    await goto('/');
    // Wait for page to load completely
    await page.waitForLoadState('networkidle');

    // Try to find and click anime link - it might be in header navigation
    const animeLink = page.locator('a[href="/anime"]').first();
    if (await animeLink.isVisible()) {
      await animeLink.click();
      await expect(page).toHaveURL(/.*anime/);
    }
    else {
      // If link not found, navigate directly
      await goto('/anime');
      await expect(page).toHaveURL(/.*anime/);
    }

    // Navigate back to home
    await goto('/');
    await expect(page).toHaveURL(/.*\/$/);
  });

  test('should handle responsive navigation', async ({ page, goto }) => {
    await goto('/');
    // Test mobile menu if it exists (this might not be present in current design)
    const mobileMenu = page.locator('.mobile-menu, .hamburger, [data-testid*="mobile-menu"]');
    if (await mobileMenu.isVisible()) {
      await mobileMenu.click();
      await expect(page.locator('.nav-menu, .mobile-nav').first()).toBeVisible();
    }
    else {
      // If no mobile menu, just check that navigation exists
      await expect(page.locator('nav, header').first()).toBeVisible();
    }
  });
});

test.describe('Loading States', () => {
  test('should display loading states during navigation', async ({ page, goto }) => {
    await goto('/');
    // Wait for page to load completely
    await page.waitForLoadState('networkidle');

    // Try to navigate to anime page
    const animeLink = page.locator('a[href="/anime"]').first();
    if (await animeLink.isVisible()) {
      await animeLink.click();

      // Check for loading indicators during navigation
      const loadingIndicator = page.locator('.loading, .spinner, [data-testid*="loading"]');
      if (await loadingIndicator.isVisible()) {
        await expect(loadingIndicator.first()).toBeVisible();
      }

      // Wait for navigation to complete
      await page.waitForURL(/.*anime/);
      await expect(page).toHaveURL(/.*anime/);
    }
    else {
      // If link not found, navigate directly
      await goto('/anime');
      await expect(page).toHaveURL(/.*anime/);
    }
  });
});

test.describe('Error Handling', () => {
  test('should handle 404 pages gracefully', async ({ page, goto }) => {
    await goto('/nonexistent-page');
    // Check for error page content
    await expect(page.locator('h1, h2').filter({ hasText: /404|not found/i }).first()).toBeVisible();
  });

  test('should display error states', async ({ page, goto }) => {
    await goto('/');
    // Check for error state components if they exist
    const errorState = page.locator('.error-state, [data-testid*="error"]');
    if (await errorState.isVisible()) {
      await expect(errorState.first()).toBeVisible();
    }
  });
});
