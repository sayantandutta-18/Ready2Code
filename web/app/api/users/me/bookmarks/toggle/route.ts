import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    return NextResponse.json({
      bookmarked: true,
      problem_id: body.problem_id,
    });
  } catch {
    return NextResponse.json({ detail: "Failed to toggle bookmark" }, { status: 400 });
  }
}
