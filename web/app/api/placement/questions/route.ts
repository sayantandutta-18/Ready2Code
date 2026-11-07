import { NextRequest, NextResponse } from "next/server";
import { PLACEMENT_QUESTIONS } from "@/lib/data/catalogs";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const track = searchParams.get("track") || "cs_core";

  const filtered = PLACEMENT_QUESTIONS.filter((q) => q.track === track || track === "all");
  return NextResponse.json(filtered.length > 0 ? filtered : PLACEMENT_QUESTIONS);
}
