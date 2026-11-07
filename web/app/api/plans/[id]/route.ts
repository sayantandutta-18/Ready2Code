import { NextRequest, NextResponse } from "next/server";
import { STUDY_PLANS, PROBLEMS } from "@/lib/data/catalogs";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  const plan = STUDY_PLANS.find((p) => p.id === id);

  if (!plan) {
    return NextResponse.json({ detail: "Study plan not found" }, { status: 404 });
  }

  // Generate days mapping
  const days: Record<number, any[]> = {};
  for (let day = 1; day <= plan.duration_days; day++) {
    const probIndex = (day - 1) % PROBLEMS.length;
    const p = PROBLEMS[probIndex];
    days[day] = [
      {
        id: p.id,
        slug: p.slug,
        title: p.title,
        difficulty: p.difficulty,
        topic: p.topic,
        solved: false,
      },
    ];
  }

  return NextResponse.json({
    id: plan.id,
    name: plan.name,
    description: plan.description,
    duration_days: plan.duration_days,
    total_problems: plan.total_problems,
    days,
    solved_count: 0,
    progress_pct: 0,
  });
}
