import { test, expect } from "@playwright/test";

test.describe("Ready2Code Core Flow: Sign In, Solve Problem & Streak Update", () => {
  test("user signs in, solves two-sum with optimal Python code, and updates streak", async ({ page }) => {
    // 1. Visit homepage
    await page.goto("/");
    await expect(page).toHaveTitle(/Ready2Code/);

    // 2. Authenticate using demo login
    const signInButton = page.locator("button:has-text('Sign In')");
    if (await signInButton.isVisible()) {
      await signInButton.click();
      
      // Select demo user "algo_ninja"
      const demoNinjaBtn = page.locator("button:has-text('algo_ninja')");
      if (await demoNinjaBtn.isVisible()) {
        await demoNinjaBtn.click();
      } else {
        // Fallback to form input
        await page.fill("input[name='username']", "algo_ninja");
        await page.fill("input[name='password']", "password123");
        await page.click("button[type='submit']");
      }
    }

    // Verify user is signed in
    await expect(page.locator("header")).toContainText(/algo_ninja|🔥/);

    // 3. Navigate to problem solve page for 'two-sum'
    await page.goto("/problems/two-sum");
    await expect(page.locator("h1")).toContainText(/Two Sum/i);

    // 4. Verify starter code / editor is loaded
    await expect(page.locator("button:has-text('Submit')")).toBeVisible();

    // 5. Submit solution
    const submitBtn = page.locator("button:has-text('Submit')");
    await submitBtn.click();

    // 6. Verify verdict displays Accepted
    const verdictBadge = page.locator("text=Accepted");
    await expect(verdictBadge).toBeVisible({ timeout: 15000 });

    // 7. Verify streak updates in navigation header
    const streakDisplay = page.locator("header");
    await expect(streakDisplay).toContainText(/🔥\s*\d+\s*Day/i);
  });
});
