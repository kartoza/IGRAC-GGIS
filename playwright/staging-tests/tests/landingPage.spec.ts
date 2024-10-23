import { test, expect } from '@playwright/test';

let url = '/';

test('test for landing page', async ({ page }) => {
  await page.goto(url);
  
  await expect(page.getByRole('heading', { name: 'The Global Groundwater' })).toBeVisible();
  await expect(page.locator('.background')).toBeVisible();
  const page1Promise = page.waitForEvent('popup');
  await page.getByRole('link', { name: 'Visit IGRAC Website' }).click();
  const page1 = await page1Promise;
  await page1.close();

  // Assertions for Features
  await expect(page.getByRole('heading', { name: 'Featured' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Transboundary Aquifers of the' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Global Groundwater Monitoring' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'MAR Portal' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Senegalo-Mauritanian Aquifer' }).first()).toBeVisible();

  await expect(page.getByRole('link', { name: 'Dinaric Karst (DIKTAS Project)' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Transboundary Aquifers (TWAP' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Small Island Developing states' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Groundwater Resources in Africa' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'Groundwater Quality ' })).toBeVisible();

  await expect(page.getByRole('link', { name: 'G3P v1.5 data' })).toBeVisible();

  await expect(page.getByRole(
    'link', { name: 'Senegalo-Mauritanian Aquifer Basin (SMAB) / Bassin Aquifère Sénégalo-Mauritanien (BASM)' }
    ).last()).toBeVisible();

});