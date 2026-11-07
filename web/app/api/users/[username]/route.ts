import { NextRequest, NextResponse } from "next/server";

export async function GET(
  request: NextRequest,
  { params }: { params: { username: string } }
) {
  const { username } = params;

  return NextResponse.json({
    id: `usr_${username}`,
    username,
    display_name: username === "algo_ninja" ? "Algo Ninja" : username === "byte_master" ? "Byte Master" : username.charAt(0).toUpperCase() + username.slice(1),
    avatar_url: null,
    timezone: "UTC",
    solved: {
      total: username === "algo_ninja" ? 42 : 24,
      easy: 15,
      medium: 8,
      hard: 1,
    },
    streak: {
      current: username === "algo_ninja" ? 7 : 3,
      longest: 14,
      freezes_left: 2,
    },
    xp: username === "algo_ninja" ? 420 : 180,
    skills: {
      "Arrays and Hashing": 8,
      "Two Pointers": 6,
      "Stack and Queue": 5,
      "Trees": 4,
      "Dynamic Programming": 2,
    },
  });
}
