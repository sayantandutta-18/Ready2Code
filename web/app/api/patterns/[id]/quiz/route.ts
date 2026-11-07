import { NextRequest, NextResponse } from "next/server";
import { PATTERNS } from "@/lib/data/catalogs";

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  const p = PATTERNS.find((x) => x.slug === id);

  if (!p) {
    return NextResponse.json({ detail: "Pattern not found" }, { status: 404 });
  }

  try {
    const body = await request.json();
    const isCorrect = body.selected_option_index === p.correct_option_index;

    return NextResponse.json({
      correct: isCorrect,
      message: isCorrect
        ? "Pattern unlocked! All problems matching this pattern are now accessible."
        : "Incorrect. Review the pattern signals and try again.",
      xp_earned: isCorrect ? 15 : 0,
    });
  } catch {
    return NextResponse.json({ detail: "Invalid request payload" }, { status: 400 });
  }
}
