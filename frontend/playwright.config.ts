import type { ConfigOptions } from '@nuxt/test-utils/playwright';

import { defineConfig, devices } from '@playwright/test';
import { fileURLToPath } from 'node:url';

async function checkDevServerRunning(url: string) {
  try {
    const res = await fetch(url);
    return res.ok;
  }
  catch {
    return false;
  }
}

const devServerUrl = 'http://localhost:3000';

const isDevServerRunning = await checkDevServerRunning(devServerUrl);

const config = defineConfig<ConfigOptions>({
  testDir: fileURLToPath(new URL('./tests/e2e', import.meta.url)),
  use: {
    nuxt: {
      rootDir: fileURLToPath(new URL('./frontend', import.meta.url)),
      host: isDevServerRunning ? devServerUrl : undefined,
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
});

if (!isDevServerRunning) {
  config.webServer = {
    command: 'pnpm run build && pnpm run preview',
    url: devServerUrl,
    reuseExistingServer: true,
  };
}

export default config;
