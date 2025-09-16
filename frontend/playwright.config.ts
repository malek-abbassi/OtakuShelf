import type { ConfigOptions } from '@nuxt/test-utils/playwright';

import { defineConfig, devices } from '@playwright/test';

export default defineConfig<ConfigOptions>({
  testDir: './tests/e2e',
  use: {
    nuxt: {
      rootDir: process.cwd(),
    },
  },
  projects: [
    // Desktop testing
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'safari',
      use: { ...devices['Desktop Safari'] },
    },
    // Mobile testing
    {
      name: 'chromium-mobile',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'safari-mobile',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'pnpm run build && pnpm run preview',
    port: 3000,
    reuseExistingServer: true,
  },
});
