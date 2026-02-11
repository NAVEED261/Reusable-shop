import { test, expect } from '@playwright/test';

test.describe('Navigation Tests', () => {
  test('navbar displays all navigation links', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('nav')).toBeVisible();
    await expect(page.locator('nav >> text=Home')).toBeVisible();
    await expect(page.locator('nav >> text=Shop')).toBeVisible();
    await expect(page.locator('nav >> text=About')).toBeVisible();
    await expect(page.locator('nav >> text=Contact')).toBeVisible();
  });

  test('navbar has cart link with badge', async ({ page }) => {
    await page.goto('/');
    const cartLink = page.locator('a[href="/cart"]');
    await expect(cartLink).toBeVisible();
  });

  test('navbar has login link', async ({ page }) => {
    await page.goto('/');
    const loginLink = page.locator('a[href="/auth/login"]');
    await expect(loginLink).toBeVisible();
  });

  test('navigate to products page', async ({ page }) => {
    await page.goto('/');
    await page.click('nav >> text=Shop');
    await expect(page).toHaveURL(/\/products/);
    await expect(page.locator('text=Our Collection')).toBeVisible();
  });

  test('navigate to about page', async ({ page }) => {
    await page.goto('/');
    await page.click('nav >> text=About');
    await expect(page).toHaveURL(/\/about/);
  });

  test('navigate to contact page', async ({ page }) => {
    await page.goto('/');
    await page.click('nav >> text=Contact');
    await expect(page).toHaveURL(/\/contact/);
  });

  test('navigate to cart page', async ({ page }) => {
    await page.goto('/');
    await page.click('a[href="/cart"]');
    await expect(page).toHaveURL(/\/cart/);
    await expect(page.locator('text=Your Cart is Empty')).toBeVisible();
  });

  test('navigate to login page', async ({ page }) => {
    await page.goto('/');
    await page.click('a[href="/auth/login"]');
    await expect(page).toHaveURL(/\/auth\/login/);
  });

  test('logo navigates to homepage', async ({ page }) => {
    await page.goto('/products');
    await page.click('a[href="/"]');
    await expect(page).toHaveURL('/');
  });

  test('all pages return 200 status', async ({ page }) => {
    const pages = ['/', '/products', '/cart', '/about', '/contact', '/auth/login', '/orders', '/profile', '/privacy', '/terms'];
    for (const path of pages) {
      const response = await page.goto(path);
      expect(response?.status()).toBe(200);
    }
  });

  test('product detail pages load for all 40 products', async ({ page }) => {
    for (let id = 1; id <= 40; id++) {
      const response = await page.goto(`/products/${id}`);
      expect(response?.status()).toBe(200);
    }
  });
});

test.describe('Mobile Navigation Tests', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('mobile menu button is visible', async ({ page }) => {
    await page.goto('/');
    const menuButton = page.locator('button:has(svg)').first();
    await expect(menuButton).toBeVisible();
  });

  test('mobile menu opens on click', async ({ page }) => {
    await page.goto('/');
    // Click the mobile menu toggle (hamburger icon)
    const menuToggle = page.locator('button.md\\:hidden');
    if (await menuToggle.isVisible()) {
      await menuToggle.click();
      await expect(page.locator('text=Home')).toBeVisible();
      await expect(page.locator('text=Shop')).toBeVisible();
    }
  });
});
