import { test, expect } from '@playwright/test';

let url = '/';

test('test for data > map-layers', async ({ page }) => {
  await page.goto(url);
  await page.getByRole('button', { name: 'Data ' }).click();
  await page.getByRole('link', { name: 'Map Layers' }).click();
  //await page.goto('https://ggis.un-igrac.org/catalogue/#/?f=dataset');
  await page.waitForLoadState('domcontentloaded');
  await expect(page.getByText('686 Resources found')).toBeVisible();
  await page.locator('li').filter({ hasText: 'DownloadPFAS contamination (' }).getByRole('link').first().click();
  await page.waitForLoadState('domcontentloaded');
  await expect(page.frameLocator('iframe').locator('canvas')).toBeVisible({timeout: 50000});
  await page.frameLocator('iframe').locator('canvas').click({
    position: {
      x: 320,
      y: 125
    }
  });

  await page.getByRole('link', { name: '' }).click();
  await expect(page.locator('li').filter({ hasText: 'DownloadGWSA_LA_hydNo' }).getByRole('link').first()).toBeVisible();
  await page.locator('li').filter({ hasText: 'DownloadGWSA_LA_hydNo' }).getByRole('link').nth(4).click();
  
  await expect(page.locator('canvas')).toBeVisible();
  await page.locator('div').filter({ hasText: /^Legend$/ }).click();
  await expect(page.locator('#map-search-bar')).toContainText('Search by location name Search by coordinates');
  
  await expect(page.getByText('::UTC +')).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^::UTC \+00$/ }).nth(1)).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^GWSA_LA_hyd$/ }).first()).toBeVisible();
  
  await expect(page.getByRole('button', { name: 'View' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Share' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Print' })).toBeVisible();
  
  await expect(page.getByRole('button', { name: 'Filter' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Download' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Measure' })).toBeVisible();
  
  await page.goto('https://ggis.un-igrac.org/catalogue/#/?f=dataset');
  await expect(page.getByRole('link', { name: 'Hydrogeological map of Guinea (Africa Groundwater Atlas, 2021)' })).toBeVisible();
  await page.getByRole('link', { name: 'Global Groundwater Monitoring' }).click();
  
  await expect(page.frameLocator('iframe').locator('canvas')).toBeVisible();
  await page.frameLocator('iframe').locator('canvas').click({
    position: {
      x: 157,
      y: 30
    }
  });
  
  await page.frameLocator('iframe').locator('canvas').click({
    position: {
      x: 185,
      y: 166
    }
  });
  
  await expect(page.locator('li').filter({ hasText: 'DownloadGlobal Groundwater' }).getByRole('link').nth(4)).toBeVisible();
  await page.locator('li').filter({ hasText: 'DownloadGlobal Groundwater' }).getByRole('link').nth(4).click();
  await expect(page.locator('section')).toBeVisible();
  
  await expect(page.locator('.gn-details-panel-header')).toBeVisible();
  await expect(page.locator('canvas')).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Legend$/ })).toBeVisible();
  
  await page.locator('span').filter({ hasText: 'Do you confirm?Are you sure' }).getByRole('img').click();
  await expect(page.locator('.background-preview-icon-frame > img').first()).toBeVisible();
  await expect(page.locator('div:nth-child(2) > .background-preview-icon-container-horizontal > .background-preview-icon-frame > img')).toBeVisible();
  
  await expect(page.locator('div:nth-child(3) > .background-preview-icon-container-horizontal > .background-preview-icon-frame > img')).toBeVisible();
  await expect(page.locator('div:nth-child(4) > .background-preview-icon-container-horizontal > .background-preview-icon-frame > img')).toBeVisible();
  await expect(page.locator('div:nth-child(4) > .background-preview-icon-container-horizontal > .background-preview-icon-frame > img')).toBeVisible();
  
  await page.getByText('Open Street Map').click();
  await expect(page.locator('canvas')).toBeVisible();
  await page.getByRole('button', { name: 'View' }).click();
  
  await page.getByRole('menuitem', { name: 'View Metadata' }).click();
  await expect(page.getByRole('heading', { name: 'Metadata : Global Groundwater' })).toBeVisible();
  await page.getByText('Identification Title Global').click();
  
  await page.locator('hr').first().click();
  await page.getByText('Identification Title Global').click();
  await page.goBack();
  
  await page.waitForLoadState('domcontentloaded');
  await page.getByRole('button', { name: 'Share' }).click();
  await expect(page.getByText('Share with people and groups')).toBeVisible();
  
  await expect(page.getByText('This page')).toBeVisible();
  await expect(page.getByRole('textbox').nth(2)).toBeVisible();
  await expect(page.getByText('Embed this Map Layer')).toBeVisible();
  
  await expect(page.getByRole('textbox').nth(3)).toBeVisible();
  await page.getByRole('button', { name: 'Share' }).click();
  await page.getByRole('button', { name: 'Print' }).click();
  
  await page.getByRole('button', { name: 'Print' }).click();
  await page.getByRole('button', { name: 'Filter' }).click();
  await expect(page.locator('.container-fluid')).toBeVisible();
  
  await expect(page.locator('div').filter({ hasText: /^Attribute filter$/ }).first()).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Area of interest$/ }).first()).toBeVisible();
  await page.locator('div').filter({ hasText: /^Select\.\.\.$/ }).nth(2).click();
  
  await page.getByRole('option', { name: 'Rectangle' }).click();
  await page.getByText('Intersects').click();
  await page.getByRole('option', { name: 'BoundingBox' }).click();
  
  await page.locator('span > .glyphicon').click();
  await page.locator('span > .glyphicon').click();
  await page.locator('#add-filter-field').click();
  
  await page.locator('.rw-i').first().click();
  await page.locator('.rw-i').first().click();
  await page.getByRole('button', { name: '' }).click();
  
  await page.getByRole('button', { name: 'Download' }).click();
  await page.getByRole('button', { name: 'Map layer' }).click();
  await expect(page.locator('div').filter({ hasText: /^Export Data$/ }).first()).toBeVisible();
  
  await expect(page.getByText('File Format')).toBeVisible();
  await expect(page.locator('#react-select-4--value')).toContainText('Select...');
  await expect(page.getByText('Spatial Reference System')).toBeVisible();
  
  await expect(page.locator('#react-select-5--value')).toContainText('Native');
  await expect(page.getByRole('button', { name: ' Export' })).toBeVisible();
  await page.getByRole('button', { name: '', exact: true }).click();
  
  await page.getByRole('button', { name: 'Measure' }).click();
  await page.getByRole('button', { name: '' }).click();
  await expect(page.locator('#measure-dialog div').filter({ hasText: 'Measure' }).first()).toBeVisible();
  
  await page.locator('#measure-dialog div').filter({ hasText: 'Measure' }).first().click();
  await expect(page.getByRole('button', { name: '' })).toBeVisible();
  await expect(page.getByRole('button', { name: '' })).toBeVisible();
  
  await page.getByRole('button', { name: '' }).click();
  await expect(page.getByRole('button', { name: '' })).toBeVisible();
  await expect(page.getByRole('button', { name: '' })).toBeVisible();
  
  await expect(page.getByRole('button', { name: '' })).toBeVisible();
  await expect(page.getByRole('button', { name: '' })).toBeVisible();
  await page.getByRole('button', { name: '', exact: true }).click();
  
  await page.getByRole('button', { name: 'Print' }).click();
  await expect(page.locator('div').filter({ hasText: /^Print$/ })).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Title$/ })).toBeVisible();
  
  await expect(page.locator('#print_preview canvas')).toBeVisible();
  await expect(page.locator('div').filter({ hasText: /^Description$/ })).toBeVisible();
  await expect(page.getByText('FormatPDF')).toBeVisible();
  
  await expect(page.getByText('Coordinates SystemEPSG:')).toBeVisible();
  await page.getByRole('button', { name: '', exact: true }).click();
  await page.getByRole('button', { name: '' }).click();
  
  await page.getByRole('button', { name: '' }).click();
  await expect(page.getByRole('tab', { name: 'Attributes' })).toBeVisible();
  await page.getByRole('tab', { name: 'Attributes' }).click();
  
  await page.getByRole('tab', { name: 'Linked Resources' }).click();
  await page.getByRole('button', { name: '' }).click();
  await page.getByTitle('Global Groundwater Monitoring').click();
  
  await page.getByTitle('Global Groundwater Monitoring').click();
});