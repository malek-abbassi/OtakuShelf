import { expect, test } from '@playwright/test';

test.describe('Watchlist Management', () => {
  test.beforeEach(async ({ page }) => {
    // Sign in before each test
    await page.goto('/auth');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.click('[data-testid="submit-button"]');

    // Wait for successful sign in
    await expect(page.locator('[data-testid="user-profile"]')).toBeVisible();
  });

  test('should navigate to watchlist page', async ({ page }) => {
    // Click the watchlist link in navigation
    await page.click('[data-testid="watchlist-link"]');

    // Should navigate to the watchlist page
    await expect(page).toHaveURL('/watchlist');

    // Should show the watchlist view
    await expect(page.locator('[data-testid="watchlist-view"]')).toBeVisible();
  });

  test('should search for anime', async ({ page }) => {
    await page.goto('/anime');

    // Search for an anime
    await page.fill('[data-testid="anime-search-input"]', 'Naruto');
    await page.click('[data-testid="search-button"]');

    // Should show search results
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
    await expect(page.locator('[data-testid="anime-card"]').first()).toBeVisible();
  });

  test('should add anime to watchlist', async ({ page }) => {
    await page.goto('/anime');

    // Search for an anime
    await page.fill('[data-testid="anime-search-input"]', 'Naruto');
    await page.click('[data-testid="search-button"]');

    // Wait for results and click on first anime
    await page.click('[data-testid="anime-card"]', { timeout: 10000 });

    // Should show anime details
    await expect(page.locator('[data-testid="anime-details"]')).toBeVisible();

    // Add to watchlist
    await page.click('[data-testid="add-to-watchlist-button"]');

    // Should show success message
    await expect(page.locator('[data-testid="success-toast"]')).toBeVisible();
  });

  test('should view and manage watchlist', async ({ page }) => {
    await page.goto('/watchlist');

    // Should show watchlist items
    await expect(page.locator('[data-testid="watchlist-item"]').first()).toBeVisible();

    // Click on edit button for first item
    await page.click('[data-testid="edit-watchlist-item"]');

    // Should open edit modal
    await expect(page.locator('[data-testid="edit-modal"]')).toBeVisible();

    // Update status
    await page.selectOption('[data-testid="status-select"]', 'completed');

    // Save changes
    await page.click('[data-testid="save-button"]');

    // Should show success message
    await expect(page.locator('[data-testid="success-toast"]')).toBeVisible();
  });

  test('should filter watchlist by status', async ({ page }) => {
    await page.goto('/watchlist');

    // Click on status filter
    await page.click('[data-testid="filter-completed"]');

    // Should filter items by completed status
    await expect(page.locator('[data-testid="watchlist-item"]')).toHaveCount(1);

    // All visible items should have completed status
    const statusBadges = page.locator('[data-testid="status-badge"]');
    await expect(statusBadges.first()).toContainText('completed');
  });

  test('should remove item from watchlist', async ({ page }) => {
    await page.goto('/watchlist');

    // Get initial count of items
    const initialCount = await page.locator('[data-testid="watchlist-item"]').count();

    // Click delete button on first item
    await page.click('[data-testid="delete-watchlist-item"]');

    // Confirm deletion
    await page.click('[data-testid="confirm-delete"]');

    // Should show success message
    await expect(page.locator('[data-testid="success-toast"]')).toBeVisible();

    // Should have one less item
    await expect(page.locator('[data-testid="watchlist-item"]')).toHaveCount(initialCount - 1);
  });

  test('should handle empty watchlist state', async ({ page }) => {
    // Navigate to a fresh user or clear watchlist
    await page.goto('/watchlist');

    // If no items, should show empty state
    const items = page.locator('[data-testid="watchlist-item"]');
    const itemCount = await items.count();

    if (itemCount === 0) {
      await expect(page.locator('[data-testid="empty-watchlist"]')).toBeVisible();
      await expect(page.locator('[data-testid="add-anime-button"]')).toBeVisible();
    }
  });

  test('should persist watchlist across browser sessions', async ({ page, context }) => {
    await page.goto('/watchlist');

    // Get current watchlist count
    const items = page.locator('[data-testid="watchlist-item"]');
    const itemCount = await items.count();

    // Close and reopen browser
    await page.close();
    const newPage = await context.newPage();

    // Sign in again
    await newPage.goto('/auth');
    await newPage.fill('[data-testid="email-input"]', 'test@example.com');
    await newPage.fill('[data-testid="password-input"]', 'password123');
    await newPage.click('[data-testid="submit-button"]');

    // Navigate to watchlist
    await newPage.goto('/watchlist');

    // Should have same number of items
    await expect(newPage.locator('[data-testid="watchlist-item"]')).toHaveCount(itemCount);
  });
});
