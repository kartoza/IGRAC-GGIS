import { test, expect } from '@playwright/test';

let url = '/';

test('test', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('link', { name: 'GeoStories' }).click();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('label').filter({ hasText: 'GeoStories' })).toBeVisible({timeout: 30000});
  await expect(page.getByText('2 Resources found')).toBeVisible();
  
  await page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first().click();
  await expect(page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first()).toBeVisible({timeout: 30000});
  await page.locator('li').filter({ hasText: 'Part 1: Discover Groundwater"' }).getByRole('link').first().click();
  await page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first().click();
  
  await expect(page.locator('li').filter({ hasText: 'Part 1: Discover Groundwater"' }).getByRole('link').first()).toBeVisible({timeout: 30000});
  await page.locator('li').filter({ hasText: 'Part 1: Discover Groundwater"' }).getByRole('link').first().click();
  await page.getByRole('tabpanel').getByText('Part 1: Discover Groundwater').click();
  
  await page.locator('div').filter({ hasText: /^View full metadata$/ }).nth(1).click();
  await expect(page.getByRole('heading', { name: 'Metadata : Part 1: Discover' })).toBeVisible({timeout: 30000});
  await page.goBack();
  
  await expect(page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first()).toBeVisible({timeout: 30000});
  await page.getByRole('link', { name: 'Part 2: The History of' }).click();
  await expect(page.getByRole('tabpanel').getByText('Part 2: The History of')).toBeVisible({timeout: 30000});
  
  await page.locator('div').filter({ hasText: /^View full metadata$/ }).nth(1).click();
  await expect(page.getByRole('heading', { name: 'Metadata : Part 2: The' })).toBeVisible({timeout: 30000});
  await expect(page.locator('dl').filter({ hasText: 'Identification Image' }).getByRole('link')).toBeVisible({timeout: 30000});
});