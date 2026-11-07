import { NextRequest, NextResponse } from "next/server";
import { INTERVIEWS } from "@/lib/data/catalogs";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const company = searchParams.get("company") || "All";
  const verdict = searchParams.get("verdict") || "All";

  let filtered = [...INTERVIEWS];

  if (company !== "All") {
    filtered = filtered.filter((i) => i.company.toLowerCase() === company.toLowerCase());
  }

  if (verdict !== "All") {
    filtered = filtered.filter((i) => i.verdict.toLowerCase() === verdict.toLowerCase());
  }

  return NextResponse.json(filtered);
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const newInterview = {
      id: `exp-${Date.now()}`,
      author: body.author || "Anonymous",
      company: body.company || "Tech Company",
      role: body.role || "Software Engineer",
      date: body.date || "November 2026",
      verdict: body.verdict || "Offer",
      ctc: body.ctc || "₹30 LPA",
      difficulty: body.difficulty || "Medium",
      rounds: body.rounds || [{ name: "Round 1", desc: "Technical DSA & Problem Solving" }],
      advice: body.advice || "Communicate clearly and write clean, modular code.",
    };

    INTERVIEWS.unshift(newInterview);
    return NextResponse.json({ status: "created", interview: newInterview });
  } catch {
    return NextResponse.json({ detail: "Invalid interview payload" }, { status: 400 });
  }
}
