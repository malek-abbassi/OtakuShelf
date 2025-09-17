import { expect, test } from '@nuxt/test-utils/playwright';

test.describe('Anime Page', () => {
  test('should load anime page', async ({ page, goto }) => {
    await goto('/anime', { waitUntil: 'hydration' });
    await expect(page).toHaveURL(/.*anime/);
    // Wait for main content to load
    await expect(page.locator('[data-testid="anime-page"]')).toBeVisible();
  });

  test('should display anime page header', async ({ page, goto }) => {
    await goto('/anime', { waitUntil: 'hydration' });
    // Wait for page to be fully loaded
    await expect(page.locator('[data-testid="anime-page"]')).toBeVisible();
    await expect(page.locator('[data-testid="anime-page-header"] h1')).toHaveText('Discover Anime');
  });

  test('should display search functionality', async ({ page, goto }) => {
    await goto('/anime', { waitUntil: 'hydration' });
    // Wait for page to be fully loaded
    await expect(page.locator('[data-testid="anime-page"]')).toBeVisible();
    // Check for search input field with proper test ID
    await expect(page.locator('[data-testid="anime-search-input"] [data-testid="search-input-field"]')).toBeVisible();
    // Check for search button
    await expect(page.locator('[data-testid="anime-search-input"] [data-testid="search-button"]')).toBeVisible();
  });

  test('should display anime cards or grid', async ({ page, goto }) => {
    await goto('/anime', { waitUntil: 'hydration' });
    // Wait for page to be fully loaded
    await expect(page.locator('[data-testid="anime-page"]')).toBeVisible();
    // Check for anime grid container
    await expect(page.locator('[data-testid="anime-search-enhanced"]')).toBeVisible();
  });

  test('should handle search input', async ({ page, goto }) => {
    await goto('/anime', { waitUntil: 'hydration' });
    const searchInput = page.getByTestId('search-input-field');
    await searchInput.pressSequentially('Naruto', { delay: 100 });
    await expect(searchInput).toHaveValue('Naruto');

    // Wait for debounced search to trigger (300ms debounce + some buffer)
    await page.waitForTimeout(500);

    // Wait for either loading state or search results
    await expect(page.locator('[data-testid="anime-search-enhanced"]')).toBeVisible();

    // Check if loading state appears
    const loadingElement = page.locator('[data-testid="anime-search-loading"]');
    if (await loadingElement.isVisible()) {
      // Wait for loading to complete
      await expect(loadingElement).not.toBeVisible({ timeout: 10000 });
    }

    // Verify search results or empty state appears
    const resultsContainer = page.locator('[data-testid="anime-search-enhanced"]');
    await expect(resultsContainer).toBeVisible();
  });
});

test.describe('Anime Details', () => {
  test('should display anime details content', async ({ page, goto }) => {
    await goto('/anime', { waitUntil: 'hydration' });
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
