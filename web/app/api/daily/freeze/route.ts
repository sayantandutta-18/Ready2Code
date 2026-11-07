import { NextResponse } from "next/server";

export async function POST() {
  return NextResponse.json({
    status: "ok",
    message: "Streak freeze activated for today. Your streak is protected!",
    freezes_left: 1,
  });
}
