import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const authHeader = request.headers.get("authorization") || request.headers.get("x-user-id");
  let username = "guest";

  if (authHeader) {
    const parts = authHeader.replace("Bearer ", "").split("_");
    if (parts.length >= 3) {
      username = parts[2];
    }
  }

  const user = {
    id: `usr_${username}`,
    username: username,
    display_name: username === "algo_ninja" ? "Algo Ninja" : username === "byte_master" ? "Byte Master" : username.charAt(0).toUpperCase() + username.slice(1),
    timezone: "UTC",
    streak: username === "algo_ninja" ? 7 : 3,
    xp: username === "algo_ninja" ? 420 : 150,
    solved_count: username === "algo_ninja" ? 14 : 5,
  };

  return NextResponse.json(user);
}
