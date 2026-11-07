import { NextResponse } from "next/server";
import { TOPICS, PROBLEMS } from "@/lib/data/catalogs";

export async function GET() {
  const topicsWithCounts = TOPICS.map((t) => {
    const count = PROBLEMS.filter((p) => {
      const pKey = (p.topic_key || "").toLowerCase();
      const pTopic = (p.topic || "").toLowerCase();
      return pKey === t.slug || pTopic.includes(t.slug) || t.name.toLowerCase().includes(pKey);
    }).length;

    return {
      id: t.id,
      slug: t.slug,
      name: t.name,
      order_index: t.order_index,
      problem_count: count > 0 ? count : t.problem_count,
    };
  });

  return NextResponse.json(topicsWithCounts);
}
