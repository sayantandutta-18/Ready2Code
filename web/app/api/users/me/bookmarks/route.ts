import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const problemId = searchParams.get("problem_id");

  return NextResponse.json({
    bookmarked: false,
    bookmarks: [],
  });
}
