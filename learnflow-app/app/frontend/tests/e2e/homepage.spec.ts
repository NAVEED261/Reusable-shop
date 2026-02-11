import { test, expect } from '@playwright/test';

test.describe('Homepage Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load homepage successfully', async ({ page }) => {
    await expect(page).toHaveTitle(/Fatima Zehra Boutique/);
  });

  test('should display hero section with branding', async ({ page }) => {
    await expect(page.locator('text=Fatima Zehra')).toBeVisible();
    await expect(page.locator('text=Boutique')).toBeVisible();
    await expect(page.locator('text=Welcome to Luxury Fashion')).toBeVisible();
  });

  test('should display Explore Collection CTA', async ({ page }) => {
    const cta = page.locator('text=Explore Collection');
    await expect(cta).toBeVisible();
    await cta.click();
    await expect(page).toHaveURL(/\/products/);
  });

  test('should display all 4 categories', async ({ page }) => {
    await expect(page.locator('text=Fancy Suits')).toBeVisible();
    await expect(page.locator('text=Shalwar Qameez')).toBeVisible();
    await expect(page.locator('text=Cotton Suits')).toBeVisible();
    await expect(page.locator('text=Designer Brands')).toBeVisible();
  });

  test('should display categories section heading', async ({ page }) => {
    await expect(page.locator('text=Browse Our Categories')).toBeVisible();
  });

  test('should display testimonials section', async ({ page }) => {
    await expect(page.locator('text=Testimonials')).toBeVisible();
    await expect(page.locator('text=Aisha Khan')).toBeVisible();
    await expect(page.locator('text=Fatima Ali')).toBeVisible();
    await expect(page.locator('text=Sara Ahmed')).toBeVisible();
  });

  test('should display trust badges', async ({ page }) => {
    await expect(page.locator('text=Free Delivery')).toBeVisible();
    await expect(page.locator('text=Secure Checkout')).toBeVisible();
    await expect(page.locator('text=Premium Quality')).toBeVisible();
  });

  test('should display CTA section', async ({ page }) => {
    await expect(page.locator('text=Ready to Find Your Perfect Suit')).toBeVisible();
  });

  test('should have no console errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') errors.push(msg.text());
    });
    await page.goto('/');
    await page.waitForTimeout(3000);
    expect(errors).toEqual([]);
  });

  test('should load hero image', async ({ page }) => {
    const heroImage = page.locator('img[alt*="Fatima Zehra"]');
    await expect(heroImage).toBeVisible();
  });

  test('should display product cards in featured sections', async ({ page }) => {
    const productCards = page.locator('[class*="ProductCard"], [class*="product"]');
    const count = await productCards.count();
    expect(count).toBeGreaterThan(0);
  });
});
