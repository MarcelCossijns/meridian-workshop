import { test, expect } from '@playwright/test'

test.describe('Reports page', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/reports')
    await expect(page.locator('.loading')).not.toBeVisible({ timeout: 8000 })
  })

  test('quarterly performance table renders Q1–Q4 rows', async ({ page }) => {
    const table = page.locator('.reports-table').first()
    await expect(table).toBeVisible()
    const rows = table.locator('tbody tr')
    await expect(rows).toHaveCount(4)
  })

  test('fulfillment rate badges carry semantic color classes', async ({ page }) => {
    const badges = page.locator('.reports-table .badge')
    await expect(badges.first()).toBeVisible()
    const count = await badges.count()
    for (let i = 0; i < count; i++) {
      const cls = await badges.nth(i).getAttribute('class')
      expect(cls).toMatch(/badge (success|warning|danger)/)
    }
  })

  test('monthly trends bar chart renders bars', async ({ page }) => {
    const bars = page.locator('.bar-chart .bar')
    await expect(bars.first()).toBeVisible()
    const count = await bars.count()
    expect(count).toBe(12)
  })

  test('summary stat cards all show non-empty values', async ({ page }) => {
    const statCards = page.locator('.stats-grid .stat-card')
    await expect(statCards).toHaveCount(4)
    for (let i = 0; i < 4; i++) {
      const value = await statCards.nth(i).locator('.stat-value').textContent()
      expect(value.trim().length).toBeGreaterThan(0)
    }
  })

  test('month-over-month table shows percentage growth rate in second row', async ({ page }) => {
    const momTable = page.locator('.reports-table').nth(1)
    await expect(momTable).toBeVisible()
    const rows = momTable.locator('tbody tr')
    const rowCount = await rows.count()
    expect(rowCount).toBeGreaterThan(1)
    const growthCell = rows.nth(1).locator('td').last()
    const text = await growthCell.textContent()
    expect(text).toMatch(/[+-]?\d+\.\d+%/)
  })

})
