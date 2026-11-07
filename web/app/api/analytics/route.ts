import { NextResponse } from "next/server";
import { TOPICS } from "@/lib/data/catalogs";

export async function GET() {
  const weekly_solves = [
    { week: "Week 1", solves: 4 },
    { week: "Week 2", solves: 7 },
    { week: "Week 3", solves: 12 },
    { week: "Week 4", solves: 9 },
  ];

  const topic_acceptance = TOPICS.map((t, idx) => ({
    topic: t.name,
    rate: Math.min(95, Math.max(50, 78 + Math.round(Math.sin(idx) * 15))),
    total_attempts: 15 + idx * 4,
  }));

  const weak_topics = [
    { topic: "Dynamic Programming", rate: 58.2, recommended_slug: "coin-change" },
    { topic: "Graphs", rate: 64.5, recommended_slug: "course-schedule" },
  ];

  return NextResponse.json({
    weekly_solves,
    topic_acceptance,
    weak_topics,
    solved_breakdown: {
      easy: 18,
      medium: 12,
      hard: 4,
      total: 34,
    },
    activity: [
      { date: "2026-11-05", count: 3 },
      { date: "2026-11-06", count: 4 },
      { date: "2026-11-07", count: 2 },
    ],
  });
}
