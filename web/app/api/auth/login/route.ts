import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const username = (body.username || "guest").trim().toLowerCase();
    const token = `r2c_tk_${username}_${Date.now()}`;

    const user = {
      id: `usr_${username}`,
      username: username,
      display_name: username === "algo_ninja" ? "Algo Ninja" : username === "byte_master" ? "Byte Master" : username.charAt(0).toUpperCase() + username.slice(1),
      timezone: "UTC",
      streak: username === "algo_ninja" ? 7 : username === "byte_master" ? 3 : 1,
      xp: username === "algo_ninja" ? 420 : username === "byte_master" ? 180 : 50,
      solved_count: username === "algo_ninja" ? 14 : username === "byte_master" ? 8 : 2,
    };

    return NextResponse.json({ token, user });
  } catch {
    return NextResponse.json({ detail: "Invalid login request" }, { status: 400 });
  }
}
