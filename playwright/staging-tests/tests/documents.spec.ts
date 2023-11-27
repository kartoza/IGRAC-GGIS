import { test, expect } from '@playwright/test';

let url = '/';

test('test', async ({ page }) => {

  await page.goto(url);

  await page.getByRole('button', { name: 'Data ' }).click();

  await page.getByRole('link', { name: 'Documents' }).click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.locator('label').filter({ hasText: 'Documents' })).toBeVisible();

  await expect(page.getByText('Filter 327 Resources found')).toBeVisible();

  await expect(page.locator('.gn-resource-card-link').first()).toBeVisible();

  await page.getByRole('link', { name: 'State of Global Water Resources Report - Quantitative status of groundwater - Annex II - Hydrographs', exact: true }).click();

  await expect(page.getByRole('tabpanel').getByText('State of Global Water')).toBeVisible();

  await page.locator('section').getByText('This is annex II of the State').click();
  
  await expect(page.locator('li:nth-child(2) > .gn-resource-card > .gn-resource-card-link')).toBeVisible();

  await page.getByRole('link', { name: 'State of Global Water Resources Report - Quantitative status of groundwater - Annex I - Algorithm', exact: true }).click();

  await expect(page.getByRole('tabpanel').getByText('State of Global Water')).toBeVisible();

  await expect(page.locator('li:nth-child(3) > .gn-resource-card > .gn-resource-card-link')).toBeVisible();

  await page.locator('#gn-catalogue').getByRole('link', { name: 'State of Global Water Resources Report - Quantitative status of groundwater -', exact: true }).click();

  await expect(page.getByRole('tabpanel').getByText('State of Global Water')).toBeVisible();

  await page.locator('li').filter({ hasText: 'DownloadWells China.Wuzhen,' }).getByRole('link').first().click();

  await expect(page.locator('li').filter({ hasText: 'DownloadWells China.Wuzhen,' }).getByRole('link').first()).toBeVisible();

  await expect(page.getByRole('tabpanel').getByText('Wells China.')).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'DownloadDeep Hand dug well -' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'DownloadOrigin of' }).getByRole('link').first()).toBeVisible();

  await page.getByRole('link', { name: '' }).click();

  await page.locator('div').filter({ hasText: /^CategoriesSelect categories$/ }).locator('span').nth(1).click();

  await page.getByLabel('Boundaries (11)').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 0 Resources found')).toBeVisible();

  await page.locator('#react-select-10--value').getByText('×').click();

  await page.locator('div').filter({ hasText: /^CategoriesSelect categories$/ }).locator('span').nth(1).click();

  await page.getByLabel('Climatology Meteorology').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 0 Resources found')).toBeVisible();

  await page.locator('#react-select-10--value').getByText('×').click();

  await page.locator('div').filter({ hasText: /^CategoriesSelect categories$/ }).locator('span').nth(1).click();

  await page.getByLabel('Inland Waters (42)').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 3 Resources found')).toBeVisible();

  await page.locator('#react-select-10--value').getByText('×').click();

  await page.locator('div').filter({ hasText: /^CategoriesSelect categories$/ }).locator('span').first().click();

  await page.getByLabel('Geoscientific Information (2)').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 0 Resources found')).toBeVisible();

  await page.locator('#react-select-10--value').getByText('×').click();

  await page.locator('div').filter({ hasText: /^KeywordsSelect keywords$/ }).locator('span').nth(1).click();

  await page.getByText('Keywords', { exact: true }).click();

  await page.locator('div').filter({ hasText: /^RegionsSelect regions$/ }).locator('span').first().click();

  await page.getByLabel('Africa (13)').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 0 Resources found')).toBeVisible();

  await page.locator('#react-select-12--value').getByText('×').click();

  await page.locator('div').filter({ hasText: /^RegionsSelect regions$/ }).locator('span').first().click();

  await page.getByLabel('Global (577)').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 121 Resources found')).toBeVisible();

  await page.locator('#react-select-12--value').getByText('×').click();

  await page.locator('div').filter({ hasText: /^OwnersSelect owners$/ }).locator('span').first().click();

  await page.getByText('Regions', { exact: true }).click();

  await page.locator('div').filter({ hasText: /^RegionsSelect regions$/ }).locator('span').nth(1).click();

  await page.getByLabel('Central African Republic (5)').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 3 Resources found')).toBeVisible();

  await page.locator('#react-select-12--value').getByText('×').click();

  await page.locator('div').filter({ hasText: /^RegionsSelect regions$/ }).locator('span').nth(1).click();

  await page.getByLabel('Democratic Republic of the').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 7 Resources found')).toBeVisible();

  await page.locator('#react-select-12--value').getByText('×').click();

  await page.locator('div').filter({ hasText: /^RegionsSelect regions$/ }).locator('span').nth(1).click();

  await page.getByLabel('Mozambique (9)').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 7 Resources found')).toBeVisible();

  await page.locator('#react-select-12--value').getByText('×').click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.getByText('Filter 327 Resources found')).toBeVisible();

});