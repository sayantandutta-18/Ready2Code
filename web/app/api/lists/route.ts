import { NextRequest, NextResponse } from "next/server";
import { LISTS, PROBLEMS } from "@/lib/data/catalogs";

export async function GET() {
  const result = LISTS.map((l) => ({
    id: l.id,
    name: l.name,
    description: l.description,
    total_problems: l.problem_slugs.length,
    solved_count: 0,
    is_system: l.is_system,
    visibility: l.visibility,
  }));

  return NextResponse.json(result);
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const newList = {
      id: `list-${Date.now()}`,
      name: body.name || "Custom List",
      description: body.description || "",
      total_problems: (body.problem_slugs || []).length,
      solved_count: 0,
      is_system: false,
      visibility: "public",
    };
    return NextResponse.json(newList);
  } catch {
    return NextResponse.json({ detail: "Invalid list payload" }, { status: 400 });
  }
}
