import { defineConfig, devices } from '@playwright/test';
export default defineConfig({
  timeout: 60000,
  expect: { timeout: 5000 },
  testDir: './tests',
  fullyParallel: true,
  reporter: [['list'], ['html', { outputFolder: 'reporting/pw-html' }]],
  use: {
    actionTimeout: 10000,
    navigationTimeout: 30000,
    baseURL: process.env.BASE_URL || 'http://localhost:5173',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    locale: process.env.DEFAULT_LOCALE || 'en-US'
  },
  projects: [
    { name: 'Chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'Firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'WebKit', use: { ...devices['Desktop Safari'] } },
  ],
});
