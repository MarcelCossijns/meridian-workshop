import { test, expect } from '@playwright/test'

test.describe('Navigation', () => {

  test('dashboard loads with page heading and KPI cards', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('.page-header h2')).toBeVisible()
    await expect(page.locator('.error')).not.toBeVisible()
    // KPI cards with non-empty values
    const kpiCards = page.locator('.kpi-card')
    await expect(kpiCards.first()).toBeVisible()
    const count = await kpiCards.count()
    for (let i = 0; i < count; i++) {
      const value = await kpiCards.nth(i).locator('.kpi-value').textContent()
      expect(value.trim().length).toBeGreaterThan(0)
    }
  })

  test('inventory page loads with data rows', async ({ page }) => {
    await page.goto('/inventory')
    await expect(page.locator('h2')).toBeVisible()
    await expect(page.locator('tbody tr').first()).toBeVisible({ timeout: 8000 })
    await expect(page.locator('.error')).not.toBeVisible()
  })

  test('orders page loads with status cards and order rows', async ({ page }) => {
    await page.goto('/orders')
    await expect(page.locator('h2')).toBeVisible()
    await expect(page.locator('.stats-grid')).toBeVisible({ timeout: 8000 })
    await expect(page.locator('tbody tr').first()).toBeVisible({ timeout: 8000 })
    await expect(page.locator('.error')).not.toBeVisible()
  })

  test('reports page loads and clears loading state', async ({ page }) => {
    await page.goto('/reports')
    await expect(page.locator('h2')).toBeVisible()
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })
    await expect(page.locator('.error')).not.toBeVisible()
  })

  test('restocking page loads with budget input', async ({ page }) => {
    await page.goto('/restocking')
    await expect(page.locator('h2')).toBeVisible()
    await expect(page.locator('.budget-input')).toBeVisible()
    await expect(page.locator('.error-state')).not.toBeVisible()
  })

  test('clicking nav links routes to correct pages', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    await page.locator('.nav-tabs a[href="/inventory"]').click()
    await expect(page).toHaveURL(/\/inventory/)
    await expect(page.locator('h2')).toBeVisible()

    await page.locator('.nav-tabs a[href="/reports"]').click()
    await expect(page).toHaveURL(/\/reports/)
    await expect(page.locator('h2')).toBeVisible()
  })

})
