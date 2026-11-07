import { NextResponse } from "next/server";
import { JOBS } from "@/lib/data/catalogs";

export async function GET() {
  return NextResponse.json(JOBS);
}
