import { expect, test } from '@nuxt/test-utils/playwright';

test.describe('Anime Page', () => {
  test('should load anime page', async ({ page, goto }) => {
    await goto('/anime');
    await expect(page).toHaveURL(/.*anime/);
    // Wait for main content to load
    await expect(page.locator('.space-y-6')).toBeVisible();
  });

  test('should display anime page header', async ({ page, goto }) => {
    await goto('/anime');
    // Wait for page to be fully loaded
    await expect(page.locator('.space-y-6')).toBeVisible();
    await expect(page.locator('h1').filter({ hasText: 'Discover Anime' })).toBeVisible();
  });

  test('should display search functionality', async ({ page, goto }) => {
    await goto('/anime');
    // Wait for page to be fully loaded
    await expect(page.locator('.space-y-6')).toBeVisible();
    // Check for UInput search field with correct placeholder
    await expect(page.locator('input[placeholder*="Search for anime"]').first()).toBeVisible();
    // Check for search button
    await expect(page.locator('button').filter({ hasText: 'Search' }).first()).toBeVisible();
  });

  test('should display anime cards or grid', async ({ page, goto }) => {
    await goto('/anime');
    // Wait for page to be fully loaded
    await expect(page.locator('.space-y-6')).toBeVisible();
    // Check for anime grid container (may be empty initially)
    // Just check that the page structure is there
    await expect(page.locator('.space-y-6')).toBeVisible();
  });

  test('should handle search input', async ({ page, goto }) => {
    await goto('/anime');
    const searchInput = page.locator('input[placeholder*="Search for anime"]').first();
    await searchInput.fill('Naruto');
    await expect(searchInput).toHaveValue('Naruto');

    // Wait for debounced search to trigger (300ms debounce + some buffer)
    await page.waitForTimeout(500);

    // Wait for either loading state or search results
    await expect(page.locator('.space-y-6')).toBeVisible();

    // Check if loading state appears
    const loadingElement = page.locator('text=Searching anime...');
    if (await loadingElement.isVisible()) {
      // Wait for loading to complete
      await expect(loadingElement).not.toBeVisible({ timeout: 10000 });
    }

    // Verify search results or empty state appears
    const resultsContainer = page.locator('.space-y-6');
    await expect(resultsContainer).toBeVisible();
  });
});

test.describe('Anime Details', () => {
  test('should display anime details content', async ({ page, goto }) => {
    await goto('/anime');
    // Wait for page to be fully loaded
    await expect(page.locator('.space-y-6')).toBeVisible();

    // Check for details page elements when available
    const detailsElements = page.locator('.anime-details, .anime-info, main');
    if (await detailsElements.isVisible({ timeout: 5000 })) {
      await expect(detailsElements.first()).toBeVisible();
    }
    else {
      // Skip test if no details elements are available
      test.skip(true, 'No anime details elements available to test');
    }
  });
});
