import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    return NextResponse.json({
      role: "Interviewer",
      response: `Good thought process. How would you optimize the space complexity if the array was already sorted in ascending order? Could we avoid allocating the hash map altogether?`,
      hint_tier: 2,
    });
  } catch {
    return NextResponse.json({ detail: "AI interview error" }, { status: 400 });
  }
}
