import { NextRequest, NextResponse } from "next/server";
import { LISTS, PROBLEMS } from "@/lib/data/catalogs";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  const list = LISTS.find((l) => l.id === id || l.name.toLowerCase() === id.toLowerCase());

  if (!list) {
    return NextResponse.json({ detail: "List not found" }, { status: 404 });
  }

  const problems = list.problem_slugs.map((slug, idx) => {
    const p = PROBLEMS.find((x) => x.slug === slug || x.id === slug);
    return {
      id: p ? p.id : `prob_${slug}`,
      slug: slug,
      title: p ? p.title : slug.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
      difficulty: p ? p.difficulty : "medium",
      topic: p ? p.topic : "General",
      position: idx + 1,
      solved: false,
    };
  });

  return NextResponse.json({
    id: list.id,
    name: list.name,
    description: list.description,
    is_system: list.is_system,
    problems,
    total_problems: problems.length,
    solved_count: 0,
    progress_pct: 0,
  });
}
