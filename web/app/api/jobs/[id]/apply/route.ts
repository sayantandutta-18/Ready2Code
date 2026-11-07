import { NextRequest, NextResponse } from "next/server";

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  return NextResponse.json({
    status: "applied",
    message: `Application submitted successfully for job position (${id})! Recruiter notified.`,
  });
}
