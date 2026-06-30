import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,
  workers: 1,
  retries: 1,
  reporter: [['html'], ['list']],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: [
    {
      command: 'cd server && uv run python main.py',
      url: 'http://localhost:8001/api/dashboard/summary',
      reuseExistingServer: true,
      timeout: 15000,
    },
    {
      command: 'cd client && npm run dev',
      url: 'http://localhost:3000',
      reuseExistingServer: true,
      timeout: 15000,
    },
  ],
})
