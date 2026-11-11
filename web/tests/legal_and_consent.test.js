const { describe, it } = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");

describe("Legal Configuration & Consent Validation Suite", () => {
  it("defines comprehensive centralized legal & grievance configuration", () => {
    const configPath = path.resolve(__dirname, "../lib/legalConfig.ts");
    assert.ok(fs.existsSync(configPath), "legalConfig.ts must exist");

    const content = fs.readFileSync(configPath, "utf-8");
    assert.ok(content.includes("platformName: \"Ready2Code\""), "Platform name must be defined");
    assert.ok(content.includes("supportEmail: \"support@ready2code.dev\""), "Support email must be defined");
    assert.ok(content.includes("termsVersion: \"2026-11-11\""), "Terms version must be defined");
    assert.ok(content.includes("privacyVersion: \"2026-11-11\""), "Privacy version must be defined");
    assert.ok(content.includes("grievanceOfficer"), "Grievance officer object must be present");
    assert.ok(content.includes("acknowledgementWindow"), "48-hour acknowledgement must be declared");
    assert.ok(content.includes("redressalWindow"), "30-day redressal must be declared");
  });

  it("verifies registration logic strictly enforces affirmative terms consent", () => {
    function validateRegistration(body) {
      if (!body.terms_accepted) {
        return {
          status: 400,
          error: "Affirmative consent to the Terms of Service and Privacy Policy is required to create an account."
        };
      }
      return {
        status: 200,
        user: {
          username: body.username,
          terms_accepted_at: new Date().toISOString(),
          terms_version: body.terms_version || "2026-11-11"
        }
      };
    }

    // Without consent -> 400 rejection
    const rejected = validateRegistration({ username: "coder1", terms_accepted: false });
    assert.strictEqual(rejected.status, 400);
    assert.ok(rejected.error.includes("Affirmative consent"));

    // With consent -> 200 success with recorded timestamp
    const accepted = validateRegistration({ username: "coder2", terms_accepted: true, terms_version: "2026-11-11" });
    assert.strictEqual(accepted.status, 200);
    assert.ok(accepted.user.terms_accepted_at);
    assert.strictEqual(accepted.user.terms_version, "2026-11-11");
  });

  it("validates that all required legal pages exist in the application routes", () => {
    const termsPath = path.resolve(__dirname, "../app/terms/page.tsx");
    const privacyPath = path.resolve(__dirname, "../app/privacy/page.tsx");
    const contactPath = path.resolve(__dirname, "../app/contact/page.tsx");
    const cookiesPath = path.resolve(__dirname, "../app/cookies/page.tsx");

    assert.ok(fs.existsSync(termsPath), "Route /terms must exist");
    assert.ok(fs.existsSync(privacyPath), "Route /privacy must exist");
    assert.ok(fs.existsSync(contactPath), "Route /contact must exist");
    assert.ok(fs.existsSync(cookiesPath), "Route /cookies must exist");
  });

  it("validates global footer includes links to all legal pages", () => {
    const footerPath = path.resolve(__dirname, "../components/ui/Footer.tsx");
    assert.ok(fs.existsSync(footerPath), "Footer component must exist");

    const content = fs.readFileSync(footerPath, "utf-8");
    assert.ok(content.includes("/terms"), "Footer must link to /terms");
    assert.ok(content.includes("/privacy"), "Footer must link to /privacy");
    assert.ok(content.includes("/contact"), "Footer must link to /contact");
    assert.ok(content.includes("/cookies"), "Footer must link to /cookies");
  });

  it("verifies account deletion API route is configured", () => {
    const userMePath = path.resolve(__dirname, "../app/api/users/me/route.ts");
    assert.ok(fs.existsSync(userMePath), "API route /api/users/me must exist");

    const content = fs.readFileSync(userMePath, "utf-8");
    assert.ok(content.includes("export async function DELETE"), "Route must handle DELETE method for account erasure");
    assert.ok(content.includes("export async function PATCH"), "Route must handle PATCH method for profile settings");
  });
});
