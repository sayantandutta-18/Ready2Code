import { NextResponse } from "next/server";
import { COMPANIES } from "@/lib/data/catalogs";

export async function GET() {
  return NextResponse.json(COMPANIES);
}
