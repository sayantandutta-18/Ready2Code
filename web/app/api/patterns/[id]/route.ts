import { NextRequest, NextResponse } from "next/server";
import { PATTERNS } from "@/lib/data/catalogs";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  const p = PATTERNS.find((x) => x.slug === id);

  if (!p) {
    return NextResponse.json({ detail: "Pattern not found" }, { status: 404 });
  }

  return NextResponse.json({
    slug: p.slug,
    name: p.name,
    signals: p.signals,
    lesson_md: p.lesson_md,
    template_code: p.template_code,
    quiz: {
      question: p.quiz_question,
      options: p.options,
    },
  });
}
