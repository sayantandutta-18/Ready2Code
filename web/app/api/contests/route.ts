import { NextResponse } from "next/server";
import { CONTESTS } from "@/lib/data/catalogs";

export async function GET() {
  const result = CONTESTS.map((c) => ({
    id: c.id,
    title: c.title,
    starts_at: c.starts_at,
    duration_min: c.duration_min,
    type: c.type,
    status: c.status,
    total_problems: c.problem_slugs.length,
  }));

  return NextResponse.json(result);
}
