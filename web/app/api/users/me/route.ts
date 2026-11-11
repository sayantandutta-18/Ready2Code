import { NextRequest, NextResponse } from "next/server";

export async function PATCH(request: NextRequest) {
  try {
    const body = await request.json();
    const { username, display_name, timezone } = body;

    if (username) {
      const clean = username.trim();
      if (clean.length < 3 || clean.length > 20) {
        return NextResponse.json({ detail: "Username must be between 3 and 20 characters." }, { status: 400 });
      }
      if (!/^[a-zA-Z0-9_]+$/.test(clean)) {
        return NextResponse.json({ detail: "Username can only contain alphanumeric characters and underscores." }, { status: 400 });
      }
    }

    return NextResponse.json({
      status: "ok",
      username: username || "coder_alex",
      display_name: display_name || "Alex Vance",
      timezone: timezone || "UTC",
    });
  } catch {
    return NextResponse.json({ detail: "Failed to update profile settings" }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest) {
  try {
    // Read authorization token
    const authHeader = request.headers.get("authorization") || "";
    const token = authHeader.replace(/^Bearer\s+/i, "").trim();

    return NextResponse.json({
      status: "ok",
      message: "Account and associated profile data have been permanently queued for deletion.",
      token_revoked: Boolean(token),
    });
  } catch {
    return NextResponse.json({ detail: "Failed to process account deletion" }, { status: 500 });
  }
}
