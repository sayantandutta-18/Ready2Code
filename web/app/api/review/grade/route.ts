import { NextResponse } from "next/server";

export async function POST() {
  return NextResponse.json({
    status: "updated",
    next_interval_days: 3,
    message: "Review recorded. Spaced-repetition interval updated.",
  });
}
