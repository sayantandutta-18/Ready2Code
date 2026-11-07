import { NextRequest, NextResponse } from "next/server";
import { PROBLEMS } from "@/lib/data/catalogs";

export async function GET(
  request: NextRequest,
  { params }: { params: { slug: string } }
) {
  const { slug } = params;
  const p = PROBLEMS.find((x) => x.slug === slug || x.id === slug);

  if (!p) {
    return NextResponse.json({ detail: "Problem not found" }, { status: 404 });
  }

  // Ensure editorial and hints are present
  const hints = Array.isArray(p.hints) && p.hints.length > 0
    ? p.hints.map((h: any, idx: number) => {
        if (typeof h === "string") {
          return { level: idx + 1, text: h };
        }
        return { level: h.level || idx + 1, text: h.text || h.hint || String(h) };
      })
    : [
        { level: 1, text: `Think about how the ${p.topic} data structure can help you maintain state efficiently.` },
        { level: 2, text: "Consider sorting or indexing using a hash table to convert an O(n^2) check into O(n)." },
        { level: 3, text: "Initialize your boundary pointers, traverse linearly, and handle null or boundary checks." }
      ];

  const editorial = {
    approach: `Optimal ${p.topic} Pattern`,
    body_md: `### Approach & Analysis for ${p.title}\n\n1. **Data Structure Strategy**: Utilize ${p.topic} to process elements in a single pass.\n2. **Time Complexity**: Optimal $O(n)$ or $O(n \\log n)$.\n3. **Space Complexity**: $O(1)$ auxiliary space or $O(n)$ for auxiliary tracking.\n\n\`\`\`python\n# Reference Solution\n${p.reference_python || p.starter_code?.python || "# Solution"}\n\`\`\``,
    complexity_time: "O(n)",
    complexity_space: "O(1)"
  };

  return NextResponse.json({
    ...p,
    hints,
    editorial,
    user_status: "todo",
  });
}
