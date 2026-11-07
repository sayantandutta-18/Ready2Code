import { NextRequest, NextResponse } from "next/server";
import { COMPANIES } from "@/lib/data/catalogs";

export async function GET(
  request: NextRequest,
  { params }: { params: { name: string } }
) {
  const { name } = params;
  const company = COMPANIES.find((c) => c.slug.toLowerCase() === name.toLowerCase());

  if (!company) {
    return NextResponse.json({ detail: "Company track not found" }, { status: 404 });
  }

  return NextResponse.json(company);
}
