import type { Metadata } from "next";
import React from "react";

type Props = {
  params: { slug: string };
  children: React.ReactNode;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const formattedTitle = params.slug
    .replace(/-/g, " ")
    .replace(/\b\w/g, (l) => l.toUpperCase());

  return {
    title: `${formattedTitle} | Ready2Code Problem Arena`,
    description: `Solve ${formattedTitle} on Ready2Code. Run code in Python, JavaScript, C++, and Java with live Judge0 verdicts and test cases.`,
    openGraph: {
      title: `${formattedTitle} | Ready2Code Problem Arena`,
      description: `Solve ${formattedTitle} with real verdicts, tiered hints, and algorithm visualizers.`,
    },
  };
}

export default function ProblemLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
