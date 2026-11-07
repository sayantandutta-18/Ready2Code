import { NextRequest, NextResponse } from "next/server";

export async function GET(
  request: NextRequest,
  { params }: { params: { slug: string } }
) {
  const { slug } = params;
  return NextResponse.json({
    problem_slug: slug,
    body_md: `# Personal Notes for ${slug}\n\n- Key trick: check boundary cases first.\n- Space-time trade-off: use hash set or sorted two pointers.`,
    updated_at: new Date().toISOString(),
  });
}

export async function POST(
  request: NextRequest,
  { params }: { params: { slug: string } }
) {
  const { slug } = params;
  try {
    const body = await request.json();
    return NextResponse.json({
      status: "saved",
      problem_slug: slug,
      body_md: body.body_md || "",
      updated_at: new Date().toISOString(),
    });
  } catch {
    return NextResponse.json({ detail: "Invalid note payload" }, { status: 400 });
  }
}
