import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
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
    };

    return NextResponse.json({ token, user });
  } catch {
    return NextResponse.json({ detail: "Registration failed" }, { status: 400 });
  }
}
