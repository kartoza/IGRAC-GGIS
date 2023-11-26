import { test, expect } from '@playwright/test';

let url = '/';

test('test', async ({ page }) => {
  await page.goto(url);

  await page.getByRole('link', { name: 'Dashboards' }).click();

  await page.waitForLoadState('domcontentloaded');

  await expect(page.locator('li').filter({ hasText: 'Trial_GGMN...Elie GergesView' }).getByRole('link').first()).toBeVisible({timeout: 30000});

  await expect(page.locator('li').filter({ hasText: 'Pie_chart_trial...Elie' }).getByRole('link').first()).toBeVisible({timeout: 30000});

  await expect(page.locator('li').filter({ hasText: 'Dashboard Population...Elie' }).getByRole('link').first()).toBeVisible({timeout: 30000});

  await page.getByRole('link', { name: 'Trial_GGMN' }).click();

  await page.frameLocator('iframe').locator('canvas').click({
    position: {
      x: 129,
      y: 53
    }
  });

  await page.frameLocator('iframe').locator('canvas').click({
    position: {
      x: 278,
      y: 200
    }
  });

  await page.frameLocator('iframe').locator('canvas').click({
    position: {
      x: 256,
      y: 210
    }
  });

  await page.locator('div').filter({ hasText: /^Title$/ }).click();

  await page.getByRole('tabpanel').getByText('Trial_GGMN').click();

  await page.locator('div').filter({ hasText: /^View full metadata$/ }).nth(1).click();

  await expect(page.getByRole('heading', { name: 'Metadata : Trial_GGMN' })).toBeVisible({timeout: 30000});

  await expect(page.getByText('Identification', { exact: true })).toBeVisible({timeout: 30000});

  await expect(page.getByText('Trial_GGMN', { exact: true })).toBeVisible({timeout: 30000});

  await page.goBack();

  await page.waitForLoadState('domcontentloaded');

  await page.getByRole('link', { name: '' }).click();

  await page.getByRole('link', { name: 'Pie_chart_trial' }).click();

  await expect(page.frameLocator('iframe').locator('canvas')).toBeVisible({timeout: 30000});

  await page.getByRole('tabpanel').getByText('Pie_chart_trial').click();

  await page.locator('div').filter({ hasText: /^View full metadata$/ }).nth(1).click();

  await expect(page.getByRole('heading', { name: 'Metadata : Pie_chart_trial' })).toBeVisible({timeout: 30000});

  await page.goBack();

  await page.getByText('Resource type').click();

  await expect(page.getByRole('tabpanel').getByRole('link', { name: 'dashboard' })).toBeVisible({timeout: 30000});

  await page.locator('li').filter({ hasText: 'Dashboard Population...Elie' }).getByRole('link').first().click();

  await page.frameLocator('iframe').locator('canvas').click({
    position: {
      x: 68,
      y: 91
    }
  });

  await expect(page.frameLocator('iframe').locator('canvas')).toBeVisible({timeout: 30000});

  await expect(page.getByRole('tabpanel').getByRole('link', { name: 'dashboard' })).toBeVisible({timeout: 30000});

  await page.getByRole('link', { name: 'View full metadata' }).click();
  
  await expect(page.getByRole('heading', { name: 'Metadata : Dashboard' })).toBeVisible({timeout: 30000});
});