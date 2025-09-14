// Global setup for Playwright tests
import type { FullConfig } from '@playwright/test';

import { chromium } from '@playwright/test';

async function globalSetup(_config: FullConfig) {
  // Launch browser for setup
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    // Wait for the backend to be ready
    await page.goto('http://localhost:8000/health', { waitUntil: 'networkidle' });

    // Wait for the frontend to be ready
    await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });

    // eslint-disable-next-line no-console
    console.log('✅ Both frontend and backend are ready for testing');
  }
  catch (error) {
    console.error('❌ Failed to connect to applications:', error);
    throw error;
  }
  finally {
    await browser.close();
  }
}

export default globalSetup;
