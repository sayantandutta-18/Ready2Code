import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    return NextResponse.json({
      status: "saved",
      problem_id: body.problem_id,
      body_md: body.body_md || "",
      updated_at: new Date().toISOString(),
    });
  } catch {
    return NextResponse.json({ detail: "Failed to save note" }, { status: 400 });
  }
}
