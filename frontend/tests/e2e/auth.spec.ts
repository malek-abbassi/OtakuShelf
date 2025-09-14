import { expect, test } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Start each test from the homepage
    await page.goto('/');
  });

  test('should navigate to auth page', async ({ page }) => {
    // Click the sign in button or link
    await page.click('[data-testid="sign-in-button"]');

    // Should navigate to the auth page
    await expect(page).toHaveURL('/auth');

    // Should show the auth form
    await expect(page.locator('[data-testid="auth-form"]')).toBeVisible();
  });

  test('should allow user to sign up', async ({ page }) => {
    await page.goto('/auth');

    // Switch to sign up mode
    await page.click('[data-testid="signup-tab"]');

    // Fill in the sign up form
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="username-input"]', 'testuser');
    await page.fill('[data-testid="fullname-input"]', 'Test User');

    // Submit the form
    await page.click('[data-testid="submit-button"]');

    // Should show success message or redirect
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  });

  test('should allow user to sign in', async ({ page }) => {
    await page.goto('/auth');

    // Fill in the sign in form
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');

    // Submit the form
    await page.click('[data-testid="submit-button"]');

    // Should redirect to dashboard or show user profile
    await expect(page).toHaveURL(/\/(dashboard|profile)/);
    await expect(page.locator('[data-testid="user-profile"]')).toBeVisible();
  });

  test('should show validation errors for invalid input', async ({ page }) => {
    await page.goto('/auth');

    // Try to submit with empty fields
    await page.click('[data-testid="submit-button"]');

    // Should show validation errors
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
  });

  test('should handle sign out', async ({ page }) => {
    // First sign in
    await page.goto('/auth');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.click('[data-testid="submit-button"]');

    // Wait for successful sign in
    await expect(page.locator('[data-testid="user-profile"]')).toBeVisible();

    // Click sign out
    await page.click('[data-testid="sign-out-button"]');

    // Should redirect to home page
    await expect(page).toHaveURL('/');
    await expect(page.locator('[data-testid="sign-in-button"]')).toBeVisible();
  });
});
