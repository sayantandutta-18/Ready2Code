import { NextResponse } from "next/server";
import { STUDY_PLANS } from "@/lib/data/catalogs";

export async function GET() {
  return NextResponse.json(STUDY_PLANS);
}
