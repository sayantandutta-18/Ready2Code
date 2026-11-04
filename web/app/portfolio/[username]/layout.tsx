import type { Metadata } from "next";
import React from "react";

type Props = {
  params: { username: string };
  children: React.ReactNode;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  return {
    title: `${params.username}'s Public Portfolio | Ready2Code`,
    description: `Verified algorithmic skill profile and developer portfolio for ${params.username}.`,
  };
}

export default function PortfolioLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
