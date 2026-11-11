import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    if (!body.terms_accepted) {
      return NextResponse.json(
        { detail: "Affirmative consent to the Terms of Service and Privacy Policy is required to create an account." },
        { status: 400 }
      );
    }
    const username = (body.username || "coder").trim().toLowerCase();
    const token = `r2c_tk_${username}_${Date.now()}`;

    const user = {
      id: `usr_${username}`,
      username: username,
      display_name: body.display_name || username.charAt(0).toUpperCase() + username.slice(1),
      timezone: body.timezone || "UTC",
      streak: 1,
      xp: 25,
      solved_count: 0,
      terms_accepted_at: new Date().toISOString(),
      terms_version: body.terms_version || "2026-11-11",
    };

    return NextResponse.json({ token, user });
  } catch {
    return NextResponse.json({ detail: "Registration failed" }, { status: 400 });
  }
}
