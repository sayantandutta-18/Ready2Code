import { NextRequest, NextResponse } from "next/server";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  return NextResponse.json({
    id,
    player1: {
      username: "you",
      rating: 1640,
    },
    player2: {
      username: "byte_master",
      rating: 1780,
    },
    problem_slug: "two-sum",
    duration_seconds: 600,
    status: "ongoing",
  });
}
