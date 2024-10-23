import { test, expect } from '@playwright/test';

let url = '/';

test('test for data > well and monitoring data', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('button', { name: 'Data ' }).click();

  await page.getByRole('link', { name: 'Well and Monitoring Data', exact: true }).click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.locator('div').filter({ hasText: /^Well and Monitoring Data$/ }).first()).toBeVisible();

  await expect(page.getByRole('button', { name: 'View' })).toBeVisible();

  await expect(page.getByRole('button', { name: 'Share' })).toBeVisible();

  await expect(page.getByRole('button', { name: 'Metadata' })).toBeVisible();

  await expect(page.getByRole('button', { name: 'Print' })).toBeVisible();

  await expect(page.getByRole('button', { name: 'Measure' })).toBeVisible();

  await expect(page.locator('canvas')).toBeVisible();

  await expect(page.locator('#mapstore-layers').getByText('Default')).toBeVisible();

  await expect(page.locator('div').filter({ hasText: /^Well and Monitoring Data$/ }).nth(2)).toBeVisible();

  await expect(page.locator('#map-search-bar')).toContainText('Search by location name Search by coordinates');

  await page.locator('canvas').click({
    position: {
      x: 924,
      y: 209
    }
  });

  await expect(page.locator('#identify-container')).toContainText('Israel Hydrological Service-97213902');

  await expect(page.frameLocator('iframe >> nth=0').locator('.highcharts-background')).toBeVisible();

  await expect(page.frameLocator('iframe >> nth=1').locator('.highcharts-background')).toBeVisible();

  await expect(page.frameLocator('iframe >> nth=2').locator('.highcharts-background')).toBeVisible();

  await expect(page.locator('.square-button > .glyphicon').first()).toBeVisible();

  await page.locator('.square-button').first().click();

  await page.locator('canvas').click({
    position: {
      x: 511,
      y: 258
    }
  });

  await page.locator('.no-border').first().click();

  await page.getByRole('button', { name: '', exact: true }).click();

  await page.getByTitle('Well and Monitoring Data').click();

  await page.getByRole('button', { name: '' }).click();

  await expect(page.getByRole('tabpanel').getByText('Well and Monitoring Data')).toBeVisible();

  await page.getByRole('button', { name: '', exact: true }).click();

  await page.getByRole('button', { name: '' }).click();

  await page.getByRole('button', { name: '' }).click();

  await page.getByRole('button', { name: 'View' }).click();

  await page.getByRole('menuitem', { name: 'View Metadata' }).click();

  await expect(page.getByRole('heading', { name: 'Metadata : Well and' })).toBeVisible();

  await expect(page.locator('#info')).toContainText('Well and Monitoring Data');

  await expect(page.locator('dl').filter({ hasText: 'Identification Image' }).getByRole('definition')).toBeVisible();

  await page.getByRole('heading', { name: 'Metadata : Well and' }).click();

  await page.getByText('× Placeholder for status-message Placeholder for status-message-body Metadata').click();

  await page.getByText('June 24, 2020, 4:25 a.m.').click();

  await page.goBack();

  await page.getByRole('button', { name: 'Share' }).click();

  await expect(page.getByText('Share with people and groups')).toBeVisible();

  await expect(page.locator('section')).toContainText('This page');

  await expect(page.locator('section')).toContainText('Embed this Map');

  await page.getByRole('button', { name: '', exact: true }).click();

  await page.getByRole('button', { name: 'Metadata' }).click();

  await expect(page.locator('#metadata-dialog div').filter({ hasText: 'Metadata×' }).first()).toBeVisible();

  await page.locator('.no-border').first().click();

  await expect(page.getByRole('heading')).toContainText('Well and Monitoring Data');

  await expect(page.locator('#info')).toContainText('References');

  await page.getByRole('button', { name: '×' }).click();

  await page.getByRole('button', { name: 'Print' }).click();

  await expect(page.locator('div').filter({ hasText: /^Print$/ })).toBeVisible();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.locator('#print_preview canvas')).toBeVisible();

  await page.locator('div').filter({ hasText: /^Print$/ }).click();

  await page.getByRole('button', { name: '', exact: true }).click();

  await expect(page.locator('#page-map-viewer').getByRole('img')).toBeVisible();

});