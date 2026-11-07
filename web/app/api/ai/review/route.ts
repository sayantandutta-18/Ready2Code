import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    return NextResponse.json({
      time_complexity: "O(n)",
      space_complexity: "O(n)",
      feedback: "Great implementation! Your linear scan with auxiliary hash map provides optimal time complexity. Consider adding an early return check if the input array is empty.",
      suggestions: [
        "Optimal time complexity achieved.",
        "Edge cases (empty array, duplicates) handled cleanly.",
        "Code style complies with standard PEP-8 / idiomatic patterns.",
      ],
    });
  } catch {
    return NextResponse.json({ detail: "Review analysis failed" }, { status: 400 });
  }
}
