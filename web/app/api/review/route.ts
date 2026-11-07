import { NextResponse } from "next/server";
import { PROBLEMS } from "@/lib/data/catalogs";

export async function GET() {
  const dueItems = PROBLEMS.slice(0, 5).map((p, idx) => ({
    id: `rev-${idx + 1}`,
    problem_id: p.id,
    slug: p.slug,
    title: p.title,
    difficulty: p.difficulty,
    topic: p.topic,
    due_date: new Date().toISOString().slice(0, 10),
    interval_days: idx + 1,
  }));

  return NextResponse.json({
    total_due: dueItems.length,
    items: dueItems,
  });
}
