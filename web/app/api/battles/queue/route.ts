import { NextResponse } from "next/server";

export async function POST() {
  const battleId = `battle-${Date.now()}`;
  return NextResponse.json({
    id: battleId,
    battle_id: battleId,
    status: "matched",
    opponent: {
      username: "byte_master",
      rating: 1780,
    },
    problem_slug: "two-sum",
  });
}
