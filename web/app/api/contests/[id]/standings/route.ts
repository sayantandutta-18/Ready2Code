import { NextResponse } from "next/server";

export async function GET() {
  const standings = [
    { rank: 1, user_id: "usr_byte_master", username: "byte_master", score: 400, penalty_min: 34, finished_at: "34m 12s" },
    { rank: 2, user_id: "usr_algo_ninja", username: "algo_ninja", score: 300, penalty_min: 42, finished_at: "42m 05s" },
    { rank: 3, user_id: "usr_code_zen", username: "code_zen", score: 300, penalty_min: 55, finished_at: "55m 20s" },
    { rank: 4, user_id: "usr_dev_sarah", username: "dev_sarah", score: 200, penalty_min: 28, finished_at: "28m 45s" },
    { rank: 5, user_id: "usr_binary_boss", username: "binary_boss", score: 200, penalty_min: 39, finished_at: "39m 10s" },
  ];

  return NextResponse.json(standings);
}
