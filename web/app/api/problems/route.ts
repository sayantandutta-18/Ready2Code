import { NextRequest, NextResponse } from "next/server";
import { PROBLEMS } from "@/lib/data/catalogs";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);

  const topic = searchParams.get("topic") || "all";
  const difficulty = searchParams.get("difficulty") || "all";
  const company = searchParams.get("company") || "all";
  const tag = searchParams.get("tag") || "all";
  const search = (searchParams.get("search") || searchParams.get("q") || "").toLowerCase().trim();
  const sortBy = searchParams.get("sort_by") || searchParams.get("sort") || "id";
  const sortOrder = searchParams.get("sort_order") || searchParams.get("order") || "asc";
  const page = parseInt(searchParams.get("page") || "1", 10);
  const limitParam = searchParams.get("limit");

  // Filter problems
  let filtered = PROBLEMS.filter((p) => {
    if (topic !== "all") {
      const pKey = (p.topic_key || "").toLowerCase();
      const pTopic = (p.topic || "").toLowerCase();
      const match = pKey === topic.toLowerCase() || pTopic.includes(topic.toLowerCase()) || pKey.replace("_", "-") === topic.toLowerCase();
      if (!match) return false;
    }

    if (difficulty !== "all" && p.difficulty.toLowerCase() !== difficulty.toLowerCase()) {
      return false;
    }

    if (tag !== "all") {
      const tags = (p.tags || []).map((t) => t.toLowerCase());
      if (!tags.includes(tag.toLowerCase())) return false;
    }

    if (search) {
      const inTitle = p.title.toLowerCase().includes(search);
      const inSlug = p.slug.toLowerCase().includes(search);
      const inTopic = p.topic.toLowerCase().includes(search);
      if (!inTitle && !inSlug && !inTopic) return false;
    }

    return true;
  });

  // Sort problems
  filtered.sort((a, b) => {
    let cmp = 0;
    if (sortBy === "difficulty") {
      const diffOrder: Record<string, number> = { easy: 1, medium: 2, hard: 3 };
      cmp = (diffOrder[a.difficulty] || 2) - (diffOrder[b.difficulty] || 2);
    } else if (sortBy === "title") {
      cmp = a.title.localeCompare(b.title);
    } else if (sortBy === "acceptance_rate") {
      cmp = a.acceptance_rate - b.acceptance_rate;
    } else if (sortBy === "runtime" || sortBy === "best_runtime_ms") {
      cmp = (a.best_runtime_ms || 50) - (b.best_runtime_ms || 50);
    } else {
      cmp = a.id.localeCompare(b.id);
    }
    return sortOrder === "desc" ? -cmp : cmp;
  });

  // If roadmap or client asks for list without limit or page=0, return array directly if requested
  if (!limitParam && !searchParams.has("page")) {
    return NextResponse.json(filtered);
  }

  const limit = parseInt(limitParam || "25", 10);
  const total = filtered.length;
  const total_pages = Math.ceil(total / limit) || 1;
  const start = (page - 1) * limit;
  const items = filtered.slice(start, start + limit);

  return NextResponse.json({
    items,
    total,
    page,
    limit,
    total_pages,
  });
}
