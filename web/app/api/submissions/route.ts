import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const problemId = searchParams.get("problem_id") || "two-sum";

  const pastSubmissions = [
    {
      id: "sub-101",
      problem_id: problemId,
      verdict: "AC",
      language: "python",
      runtime_ms: 38,
      memory_kb: 14200,
      percentile: 92.4,
      submitted_at: new Date(Date.now() - 3600 * 1000).toISOString(),
    },
    {
      id: "sub-100",
      problem_id: problemId,
      verdict: "AC",
      language: "python",
      runtime_ms: 45,
      memory_kb: 14400,
      percentile: 84.1,
      submitted_at: new Date(Date.now() - 24 * 3600 * 1000).toISOString(),
    },
  ];

  return NextResponse.json(pastSubmissions);
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const problemId = body.problem_id;
    const runtime = 35 + Math.floor(Math.random() * 20);
    const memory = 14100 + Math.floor(Math.random() * 500);

    return NextResponse.json({
      id: `sub-${Date.now()}`,
      problem_id: problemId,
      verdict: "AC",
      status: "Accepted",
      runtime_ms: runtime,
      memory_kb: memory,
      percentile: 94.2,
      tests_passed: 12,
      tests_total: 12,
      xp_awarded: 30,
      message: "Accepted! All test cases passed.",
    });
  } catch {
    return NextResponse.json({ detail: "Submission failed" }, { status: 400 });
  }
}
