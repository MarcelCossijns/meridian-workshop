import { test, expect } from '@playwright/test'

test.describe('Restocking page', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/restocking')
    await expect(page.locator('.loading-state')).not.toBeVisible({ timeout: 8000 })
  })

  test('renders recommendations table with data rows', async ({ page }) => {
    const table = page.locator('table')
    await expect(table).toBeVisible()
    const rows = table.locator('tbody tr')
    await expect(rows.first()).toBeVisible()
    const count = await rows.count()
    expect(count).toBeGreaterThan(0)
  })

  test('summary card shows items recommended and total cost', async ({ page }) => {
    const summary = page.locator('.summary-card')
    await expect(summary).toBeVisible()
    const items = await summary.locator('.summary-item').count()
    expect(items).toBe(3)
    // Each summary value should be non-empty
    for (let i = 0; i < 3; i++) {
      const val = await summary.locator('.summary-value').nth(i).textContent()
      expect(val.trim().length).toBeGreaterThan(0)
    }
  })

  test('entering a budget shows progress bar', async ({ page }) => {
    await page.locator('.budget-input').fill('50000')
    await expect(page.locator('.budget-progress-track')).toBeVisible()
    await expect(page.locator('.budget-progress-fill')).toBeVisible()
  })

  test('budget below minimum item cost shows no recommendations and no error', async ({ page }) => {
    // Min item cost is ~$16,736 — a $1 budget fits nothing
    await page.locator('.budget-input').fill('1')
    // Watcher has 600ms debounce; poll until summary updates rather than using fixed wait
    await expect(page.locator('.summary-value').first()).toHaveText('0', { timeout: 5000 })
    await expect(page.locator('.error-state')).not.toBeVisible()
  })

})
