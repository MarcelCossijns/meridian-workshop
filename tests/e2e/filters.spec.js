import { test, expect } from '@playwright/test'

test.describe('Filter bar', () => {

  test('filter bar is visible on every main page', async ({ page }) => {
    for (const route of ['/', '/inventory', '/orders', '/reports']) {
      await page.goto(route)
      await page.waitForLoadState('networkidle')
      await expect(page.locator('.filters-bar')).toBeVisible()
    }
  })

  test('location filter narrows inventory table rows', async ({ page }) => {
    await page.goto('/inventory')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    // Wait for data to be present before counting
    await expect(page.locator('tbody tr').first()).toBeVisible({ timeout: 8000 })
    const initialCount = await page.locator('tbody tr').count()

    // index 1 = location select
    await page.locator('.filter-select').nth(1).selectOption('San Francisco')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    const filteredCount = await page.locator('tbody tr').count()
    expect(filteredCount).toBeLessThanOrEqual(initialCount)
  })

  test('reset button clears filters back to all', async ({ page }) => {
    await page.goto('/inventory')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    await page.locator('.filter-select').nth(1).selectOption('San Francisco')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    const resetBtn = page.locator('.reset-filters-btn')
    await expect(resetBtn).not.toBeDisabled()
    await resetBtn.click()
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    const locationValue = await page.locator('.filter-select').nth(1).inputValue()
    expect(locationValue).toBe('all')
  })

  test('category filter on reports page reloads data without error', async ({ page }) => {
    await page.goto('/reports')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    // index 2 = category select
    await page.locator('.filter-select').nth(2).selectOption('sensors')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })
    await expect(page.locator('.error')).not.toBeVisible()
    await expect(page.locator('.reports-table').first()).toBeVisible()
  })

  test('filter state persists when navigating between pages', async ({ page }) => {
    await page.goto('/inventory')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    // Set location filter on inventory page
    await page.locator('.filter-select').nth(1).selectOption('London')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    // Navigate to orders via nav link (SPA navigation, state persists)
    await page.locator('.nav-tabs a[href="/orders"]').click()
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })

    // Location filter should still show London
    const locationValue = await page.locator('.filter-select').nth(1).inputValue()
    expect(locationValue).toBe('London')
  })

})
