import { test, expect } from '@playwright/test';

let url = '/';

test('test', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('link', { name: 'Maps' }).click();

  await page.waitForLoadState('domcontentloaded');

  await page.locator('label').filter({ hasText: 'Maps' }).isVisible();

  await page.getByLabel('Maps').isEnabled();
  
  await expect(page.getByText('18 Resources found')).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'PFAS Contamination (2023)The' }).getByRole('link').first()).toBeVisible();

  await page.locator('li').filter({ hasText: 'Population_Trial_2...Elie' }).getByRole('link').first().click();

  await expect(page.frameLocator('iframe').locator('#ms-container div').first()).toBeVisible();
  
  await expect(page.getByRole('tabpanel').getByText('Population_Trial_2')).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Population_Dashboard...Elie' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'The World Map...Elie' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Senegalo-Mauritanian Aquifer' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'G3P v1.5 dataThe G3P portal' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'DEEPWATER-CE - Climate' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Groundwater Resources in AfricaThis map viewer contains data and information on' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Small Island Developing States (TWAP)The SIDS viewer provides groundwater' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Global Groundwater Monitoring' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Global Country DataThe Global' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Transboundary Aquifers (TWAP' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Transboundary Aquifers of the' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'MAR PortalThe MAR Portal' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Groundwater QualityGlobal' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Groundwater StressGlobal' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Dinaric Karst (DIKTAS Project' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Well and Monitoring DataWell' }).getByRole('link').first()).toBeVisible();

  await expect(page.getByText('18 Resources found')).toBeVisible();
  
  await page.getByRole('link', { name: '' }).click();

  await page.getByLabel('Maps').uncheck();

  await expect(page.getByText('Resources found')).toBeVisible();

  await page.getByLabel('Featured').check();

  await expect(page.getByText('Resources found')).toBeVisible();

  await page.getByLabel('Featured').uncheck();

  await page.getByLabel('Map layersVectorRasterRemoteTime series').check();

  await page.getByLabel('Vector', { exact: true }).check();

  await page.getByLabel('Raster', { exact: true }).check();

  await page.getByLabel('Remote', { exact: true }).check();

  await page.getByLabel('Time series', { exact: true }).check();

  await page.getByText('Resources found').click();

  await page.getByLabel('Map layersVectorRasterRemoteTime series').uncheck();

  await page.getByLabel('Vector', { exact: true }).check();

  await page.getByLabel('Map layersVectorRasterRemoteTime series').uncheck();

  await page.getByLabel('Documents').check();

  await expect(page.getByText('Resources found')).toBeVisible();

  await page.getByLabel('Documents').uncheck();

  await page.getByLabel('GeoStories').check();

  await page.getByText('Resources found').click();

  await expect(page.locator('li').filter({ hasText: 'Part 2: The History of' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Part 1: Discover Groundwater"' }).getByRole('link').first()).toBeVisible();

  await page.getByLabel('GeoStories').uncheck();

  await page.getByLabel('Dashboards').check();

  await expect(page.locator('li').filter({ hasText: 'Trial_GGMN...Elie GergesView' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Pie_chart_trial...Elie' }).getByRole('link').first()).toBeVisible();

  await expect(page.locator('li').filter({ hasText: 'Dashboard Population...Elie' }).getByRole('link').first()).toBeVisible();

  await page.getByLabel('Dashboards').uncheck();

  await expect(page.getByText('Categories', { exact: true })).toBeVisible();

  await expect(page.locator('#react-select-10--value')).toContainText('Select categories');

  await expect(page.locator('#react-select-11--value')).toContainText('Select keywords');

  await expect(page.locator('#react-select-12--value')).toContainText('Select regions');

  await expect(page.locator('#react-select-13--value')).toContainText('Select owners');

  await expect(page.locator('#rw_5_input')).toBeEmpty();

  await page.getByLabel('Extent').check();

  await page.goto('https://ggis.un-igrac.org/catalogue/#/?extent=-180.0000%2C-89.3878%2C180.0000%2C76.4603');

  await expect(page.locator('canvas')).toBeVisible();

  await expect(page.getByText('© OpenStreetMap contributors.')).toBeVisible();

  await page.getByRole('button', { name: 'Clear filters' }).click();

  await expect(page.getByText('1,036 Resources found')).toBeVisible();

});