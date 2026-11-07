import { NextResponse } from "next/server";
import { PATTERNS } from "@/lib/data/catalogs";

export async function GET() {
  const result = PATTERNS.map((p) => ({
    slug: p.slug,
    name: p.name,
    order_index: p.order_index,
    signals: p.signals,
  }));

  return NextResponse.json(result);
}
