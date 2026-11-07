import { NextRequest, NextResponse } from "next/server";
import { CONTESTS, PROBLEMS } from "@/lib/data/catalogs";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  const contest = CONTESTS.find((c) => c.id === id);

  if (!contest) {
    return NextResponse.json({ detail: "Contest not found" }, { status: 404 });
  }

  const problems = contest.problem_slugs.map((slug, idx) => {
    const p = PROBLEMS.find((x) => x.slug === slug || x.id === slug);
    return {
      id: p ? p.id : `contest_prob_${slug}`,
      slug: slug,
      title: p ? p.title : slug.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
      difficulty: p ? p.difficulty : "medium",
      points: (idx + 1) * 100,
      position: idx + 1,
    };
  });

  return NextResponse.json({
    id: contest.id,
    title: contest.title,
    starts_at: contest.starts_at,
    duration_min: contest.duration_min,
    type: contest.type,
    status: contest.status,
    problems,
  });
}
