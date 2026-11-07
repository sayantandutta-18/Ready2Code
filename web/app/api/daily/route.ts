import { NextResponse } from "next/server";
import { PROBLEMS } from "@/lib/data/catalogs";

export async function GET() {
  const todayStr = new Date().toISOString().slice(0, 10);

  // Deterministically select a problem based on day
  const dateHash = todayStr.split("-").reduce((acc, part) => acc + parseInt(part, 10), 0);
  const selectedIndex = dateHash % PROBLEMS.length;
  const p = PROBLEMS[selectedIndex] || PROBLEMS[0];

  return NextResponse.json({
    date: todayStr,
    problem: {
      id: p.id,
      slug: p.slug,
      title: p.title,
      difficulty: p.difficulty,
      topic: p.topic,
    },
    streak: 7,
    solved_today: false,
    freezes_left: 2,
  });
}
