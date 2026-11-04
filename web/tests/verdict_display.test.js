const { describe, it } = require("node:test");
const assert = require("node:assert");

// Pure verdict formatting and display logic matching web/components/ui/VerdictBadge.tsx
// and web/app/problems/[slug]/page.tsx
const VERDICT_CONFIGS = {
  AC: {
    label: "Accepted",
    color: "emerald",
    bg: "bg-emerald-500/15",
    text: "text-emerald-400",
    border: "border-emerald-500/30",
  },
  WA: {
    label: "Wrong Answer",
    color: "rose",
    bg: "bg-rose-500/15",
    text: "text-rose-400",
    border: "border-rose-500/30",
  },
  TLE: {
    label: "Time Limit Exceeded",
    color: "amber",
    bg: "bg-amber-500/15",
    text: "text-amber-400",
    border: "border-amber-500/30",
  },
  RE: {
    label: "Runtime Error",
    color: "orange",
    bg: "bg-orange-500/15",
    text: "text-orange-400",
    border: "border-orange-500/30",
  },
  CE: {
    label: "Compilation Error",
    color: "purple",
    bg: "bg-purple-500/15",
    text: "text-purple-400",
    border: "border-purple-500/30",
  },
};

function getVerdictConfig(verdict) {
  const v = (verdict || "WA").toUpperCase();
  return VERDICT_CONFIGS[v] || VERDICT_CONFIGS["WA"];
}

function formatSubmissionBanner(verdict) {
  const config = getVerdictConfig(verdict.verdict);
  return {
    badgeText: config.label,
    badgeColor: config.color,
    runtimeDisplay: `${verdict.runtime_ms} ms`,
    memoryDisplay: `${Math.round(verdict.memory_kb / 1024 * 10) / 10} MB`,
    percentileDisplay: `Beats ${verdict.runtime_percentile}%`,
    isSuccess: verdict.verdict === "AC",
  };
}

function maskTestCasesForClient(testResults) {
  return testResults.map((t, idx) => {
    if (t.is_hidden) {
      return {
        test_index: idx + 1,
        is_hidden: true,
        verdict: t.verdict,
        runtime_ms: t.runtime_ms,
        passed: t.passed,
        // Hidden inputs and outputs are never rendered or leaked to the client
        input: "[Hidden Test Case]",
        expected_output: "[Hidden]",
        actual_output: t.passed ? "[Hidden]" : "[Output differs on hidden case]",
      };
    }
    return {
      test_index: idx + 1,
      is_hidden: false,
      verdict: t.verdict,
      runtime_ms: t.runtime_ms,
      passed: t.passed,
      input: t.input,
      expected_output: t.expected_output,
      actual_output: t.actual_output,
    };
  });
}

describe("Solve Page Verdict Display Suite", () => {
  it("resolves correct badge style and label for all standard verdicts", () => {
    assert.strictEqual(getVerdictConfig("AC").label, "Accepted");
    assert.strictEqual(getVerdictConfig("AC").color, "emerald");

    assert.strictEqual(getVerdictConfig("WA").label, "Wrong Answer");
    assert.strictEqual(getVerdictConfig("WA").color, "rose");

    assert.strictEqual(getVerdictConfig("TLE").label, "Time Limit Exceeded");
    assert.strictEqual(getVerdictConfig("TLE").color, "amber");

    assert.strictEqual(getVerdictConfig("RE").label, "Runtime Error");
    assert.strictEqual(getVerdictConfig("RE").color, "orange");

    assert.strictEqual(getVerdictConfig("CE").label, "Compilation Error");
    assert.strictEqual(getVerdictConfig("CE").color, "purple");
  });

  it("formats successful submission banner with runtime, memory, and percentile", () => {
    const verdict = {
      verdict: "AC",
      runtime_ms: 22,
      memory_kb: 14200,
      runtime_percentile: 94.6,
    };

    const banner = formatSubmissionBanner(verdict);
    assert.strictEqual(banner.badgeText, "Accepted");
    assert.strictEqual(banner.runtimeDisplay, "22 ms");
    assert.strictEqual(banner.memoryDisplay, "13.9 MB");
    assert.strictEqual(banner.percentileDisplay, "Beats 94.6%");
    assert.strictEqual(banner.isSuccess, true);
  });

  it("formats failed submission banner with appropriate error verdict", () => {
    const verdict = {
      verdict: "TLE",
      runtime_ms: 2000,
      memory_kb: 18000,
      runtime_percentile: 0.0,
    };

    const banner = formatSubmissionBanner(verdict);
    assert.strictEqual(banner.badgeText, "Time Limit Exceeded");
    assert.strictEqual(banner.badgeColor, "amber");
    assert.strictEqual(banner.isSuccess, false);
  });

  it("strictly masks hidden test case input and output from display", () => {
    const rawTests = [
      { is_hidden: false, verdict: "AC", runtime_ms: 12, passed: true, input: "[2,7,11,15]\n9", expected_output: "[0,1]", actual_output: "[0,1]" },
      { is_hidden: true, verdict: "WA", runtime_ms: 18, passed: false, input: "[-1000000000, 1000000000]\n0", expected_output: "[0,1]", actual_output: "[]" },
    ];

    const masked = maskTestCasesForClient(rawTests);
    assert.strictEqual(masked.length, 2);
    // Sample test preserved
    assert.strictEqual(masked[0].input, "[2,7,11,15]\n9");
    assert.strictEqual(masked[0].expected_output, "[0,1]");

    // Hidden test strictly masked
    assert.strictEqual(masked[1].is_hidden, true);
    assert.strictEqual(masked[1].input, "[Hidden Test Case]");
    assert.strictEqual(masked[1].expected_output, "[Hidden]");
    assert.ok(!masked[1].input.includes("-1000000000"));
  });
});
