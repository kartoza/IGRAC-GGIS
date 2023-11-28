import { test, expect } from '@playwright/test';

let url = '/';

test('test for geostories', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('link', { name: 'GeoStories' }).click();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.locator('label').filter({ hasText: 'GeoStories' })).toBeVisible();
  await expect(page.getByText('2 Resources found')).toBeVisible();
  
  await page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first().click();
  await expect(page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first()).toBeVisible();
  await page.locator('li').filter({ hasText: 'Part 1: Discover Groundwater"' }).getByRole('link').first().click();
  await page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first().click();
  
  await expect(page.locator('li').filter({ hasText: 'Part 1: Discover Groundwater"' }).getByRole('link').first()).toBeVisible();
  await page.locator('li').filter({ hasText: 'Part 1: Discover Groundwater"' }).getByRole('link').first().click();
  await page.getByRole('tabpanel').getByText('Part 1: Discover Groundwater').click();
  
  await page.locator('div').filter({ hasText: /^View full metadata$/ }).nth(1).click();
  await expect(page.getByRole('heading', { name: 'Metadata : Part 1: Discover' })).toBeVisible();
  await page.goBack();
  
  await expect(page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first()).toBeVisible();
  await page.getByRole('link', { name: 'Part 2: The History of' }).click();
  await expect(page.getByRole('tabpanel').getByText('Part 2: The History of')).toBeVisible();
  
  await page.locator('div').filter({ hasText: /^View full metadata$/ }).nth(1).click();
  await expect(page.getByRole('heading', { name: 'Metadata : Part 2: The' })).toBeVisible();
  await expect(page.locator('dl').filter({ hasText: 'Identification Image' }).getByRole('link')).toBeVisible();
});